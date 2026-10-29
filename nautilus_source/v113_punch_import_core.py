from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
match=re.search(r"\bint\s+importClock\s*\(\s*InputStream\s+in\s*\)\s*throws\s+Exception\s*\{",s)
assert match,"Existing Attendance logs importer not found"
start=match.start()
brace=s.index("{",match.start())
depth=0
quote=None
escape=False
end=None
for i in range(brace,len(s)):
    c=s[i]
    if quote:
        if escape:escape=False
        elif c=="\\":escape=True
        elif c==quote:quote=None
        continue
    if c in ("'",'"'):quote=c;continue
    if c=="{":depth+=1
    elif c=="}":
        depth-=1
        if depth==0:
            end=i+1
            break
assert end is not None
original=s[start:end]
assert "insertWithOnConflict" in original and "punches" in original,"Unexpected legacy import implementation"
new=r'''int importClock(InputStream in)throws Exception{
  // Independently tested SpreadsheetML 2003 punch parser. Unknown/invalid dates
  // are reported rather than silently importing zero rows as a successful operation.
  java.util.ArrayList<ClockPunchCore.Punch> punches=ClockPunchCore.parse(in);
  SQLiteDatabase writable=db.getWritableDatabase();
  int added=0;
  writable.beginTransaction();
  try{
   for(ClockPunchCore.Punch punch:punches){
    ContentValues person=new ContentValues();
    person.put("id",punch.id);
    person.put("name",punch.name.isEmpty()?"Empleado "+punch.id:punch.name);
    person.put("active",1);
    writable.insertWithOnConflict("people",null,person,SQLiteDatabase.CONFLICT_IGNORE);
    if(!punch.name.isEmpty()){
     // Do not overwrite names deliberately edited in the personnel master.
     writable.execSQL("UPDATE people SET name=? WHERE id=? AND (name IS NULL OR TRIM(name)='' OR name LIKE 'Empleado %')",
       new Object[]{punch.name,punch.id});
    }
    ContentValues mark=new ContentValues();
    mark.put("person_id",punch.id);
    mark.put("stamp",punch.stamp);
    mark.put("device",punch.device);
    if(writable.insertWithOnConflict("punches",null,mark,SQLiteDatabase.CONFLICT_IGNORE)!=-1)added++;
   }
   writable.setTransactionSuccessful();
  }finally{writable.endTransaction();}
  return added;
 }'''
s=s[:start]+new+s[end:]
p.write_text(s)
core=Path(__file__).with_name("excel_core")/"ClockPunchCore.java"
p.with_name("ClockPunchCore.java").write_bytes(core.read_bytes())
print("V113: real Attendance logs importer now uses tested XML parser and preserves manually edited employee names")
