from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
old='''   mtAddLink("▣",day,start.equals("FRANCO")?"FRANCO · "+regime:start+" — "+end+" · "+regime,()->rsEditDay(pid,day));'''
new='''   String scheduledLabel=start.equals("FRANCO")?"FRANCO · "+regime:
     "ENTRADA PROGRAMADA "+start+"  |  SALIDA PROGRAMADA "+end+"  · "+regime;
   Cursor marks=db.getReadableDatabase().rawQuery(
     "SELECT COUNT(*),MIN(substr(stamp,12,5)),MAX(substr(stamp,12,5)) FROM punches WHERE person_id=? AND substr(stamp,1,10)=?",
     new String[]{pid,day});
   int count=0;String first="",last="";
   try{if(marks.moveToFirst()){count=marks.getInt(0);first=marks.getString(1);last=marks.getString(2);}}finally{marks.close();}
   final String status=count==0?"SIN FICHADAS IMPORTADAS":
     count==1?"UNA FICHADA "+first+" · REVISAR ENTRADA/SALIDA":
     "PRIMERA FICHADA "+first+"  |  ULTIMA FICHADA "+last+"  ("+count+" marcas)";
   mtAddLink("▣",day+" · "+scheduledLabel,status,()->rsEditDay(pid,day));'''
assert old in s, "V116: scheduled-day UI anchor not found; inspect latest master, do not silently skip"
s=s.replace(old,new,1)
p.write_text(s)
print("V116: explicit scheduled entrance/exit and imported first/last punch per employee/day")
