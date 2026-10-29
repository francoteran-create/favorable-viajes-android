from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 void ensurePersonnelMaster(){
  android.database.sqlite.SQLiteDatabase x=db.getWritableDatabase();
  String[] cols={"dni TEXT","cuil TEXT","phone TEXT","address TEXT","birth_date TEXT","hire_date TEXT","job_title TEXT","emergency_contact TEXT","photo_uri TEXT","notes TEXT"};
  for(String def:cols){try{x.execSQL("ALTER TABLE people ADD COLUMN "+def);}catch(Exception ignored){}}
  x.execSQL("CREATE TABLE IF NOT EXISTS personnel_assignments(id INTEGER PRIMARY KEY AUTOINCREMENT,person_id TEXT NOT NULL,sector TEXT,regime_id TEXT,valid_from TEXT NOT NULL,valid_to TEXT,job_title TEXT,notes TEXT)");
 }
 String[] personMaster(String pid){
  ensurePersonnelMaster();String[] a={"","","","","","","","","","","",""};
  Cursor c=db.getReadableDatabase().rawQuery("SELECT name,sector,regime_id,COALESCE(dni,''),COALESCE(cuil,''),COALESCE(phone,''),COALESCE(address,''),COALESCE(birth_date,''),COALESCE(hire_date,''),COALESCE(job_title,''),COALESCE(emergency_contact,''),COALESCE(photo_uri,'') FROM people WHERE id=?",new String[]{pid});
  if(c.moveToFirst())for(int i=0;i<a.length;i++)a[i]=c.getString(i);c.close();return a;
 }
 void personnelMasterForm(String pid){
  ensurePersonnelMaster();String[] a=personMaster(pid);base("FICHA DEL PERSONAL");body.addView(refHero(a[0].isEmpty()?pid:a[0],a[1].isEmpty()?"PENDIENTE DE SECTOR":a[1]));
  String[] labs={"Nombre y apellido","DNI","CUIL","Teléfono","Domicilio","Fecha nacimiento","Fecha ingreso","Puesto / función","Contacto emergencia","Sector","Régimen"};
  String[] vals={a[0],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10],a[1],a[2]};final EditText[] e=new EditText[labs.length];
  for(int i=0;i<labs.length;i++){TextView l=label(labs[i],10);l.setTextColor(Color.rgb(160,185,195));body.addView(l);e[i]=new EditText(this);e[i].setText(vals[i]);e[i].setTextColor(Color.WHITE);e[i].setHintTextColor(Color.GRAY);e[i].setBackground(refBg(Color.rgb(13,38,49),Color.rgb(35,71,84),16));e[i].setPadding(14,10,14,10);body.addView(e[i]);}
  btn("GUARDAR FICHA COMPLETA",()->{String oldSector=a[1],oldReg=a[2],today=new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(new Date());android.content.ContentValues v=new android.content.ContentValues();v.put("name",e[0].getText().toString());v.put("dni",e[1].getText().toString());v.put("cuil",e[2].getText().toString());v.put("phone",e[3].getText().toString());v.put("address",e[4].getText().toString());v.put("birth_date",e[5].getText().toString());v.put("hire_date",e[6].getText().toString());v.put("job_title",e[7].getText().toString());v.put("emergency_contact",e[8].getText().toString());v.put("sector",e[9].getText().toString());v.put("regime_id",e[10].getText().toString());db.getWritableDatabase().update("people",v,"id=?",new String[]{pid});
   if(!oldSector.equals(e[9].getText().toString())||!oldReg.equals(e[10].getText().toString())){db.getWritableDatabase().execSQL("UPDATE personnel_assignments SET valid_to=date(?,'-1 day') WHERE person_id=? AND valid_to IS NULL",new Object[]{today,pid});android.content.ContentValues h=new android.content.ContentValues();h.put("person_id",pid);h.put("sector",e[9].getText().toString());h.put("regime_id",e[10].getText().toString());h.put("valid_from",today);h.put("job_title",e[7].getText().toString());db.getWritableDatabase().insert("personnel_assignments",null,h);}notice("Ficha guardada");employeeProfile(pid);});
  btn("FOTO DEL EMPLEADO",()->pickEmployeePhoto(pid));btn("VER DIAGRAMA DEL MES",()->employeeSchedule(pid));
 }
 String photoPersonPending=null;
 void pickEmployeePhoto(String pid){photoPersonPending=pid;Intent i=new Intent(Intent.ACTION_OPEN_DOCUMENT);i.setType("image/*");i.addCategory(Intent.CATEGORY_OPENABLE);startActivityForResult(i,902);}
 void saveEmployeePhoto(android.net.Uri uri){if(photoPersonPending==null)return;try{getContentResolver().takePersistableUriPermission(uri,Intent.FLAG_GRANT_READ_URI_PERMISSION);}catch(Exception ignored){}android.content.ContentValues v=new android.content.ContentValues();v.put("photo_uri",uri.toString());db.getWritableDatabase().update("people",v,"id=?",new String[]{photoPersonPending});String p=photoPersonPending;photoPersonPending=null;notice("Foto guardada");personnelMasterForm(p);}
 String sectorForDate(String pid,String day){
  ensurePersonnelMaster();Cursor c=db.getReadableDatabase().rawQuery("SELECT sector FROM personnel_assignments WHERE person_id=? AND valid_from<=? AND (valid_to IS NULL OR valid_to>=?) ORDER BY valid_from DESC LIMIT 1",new String[]{pid,day,day});if(c.moveToFirst()){String x=c.getString(0);c.close();return x;}c.close();Cursor p=db.getReadableDatabase().rawQuery("SELECT sector FROM people WHERE id=?",new String[]{pid});String x=p.moveToFirst()?p.getString(0):"";p.close();return x;
 }
'''
s=s.replace(mark,code+"\n"+mark)
# ensure DB extension before normal screens
s=s.replace('super.onCreate(b);','super.onCreate(b);ensurePersonnelMaster();',1)
# add master data access to profile
needle='employeeMetricStrip(pid);'
# only first day profile occurrence gets button; harmless and direct
if needle in s:s=s.replace(needle,needle+'btn("FICHA COMPLETA",()->personnelMasterForm(pid));',1)
# photo result hook before existing activity result body if available
sig='protected void onActivityResult(int requestCode,int resultCode,Intent data){'
if sig in s and 'requestCode==902' not in s:
 s=s.replace(sig,sig+'if(requestCode==902&&resultCode==RESULT_OK&&data!=null&&data.getData()!=null){saveEmployeePhoto(data.getData());return;}',1)
s=s.replace('V25 DIAGRAM ROSTER','V26 PERSONNEL MASTER')
p.write_text(s)
print("V26 personnel master applied")
