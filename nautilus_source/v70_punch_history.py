from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void dualClockHub(){'
assert mark in s
code=r'''
 void importedPunchHistory(){
  currentScreen="FICHADAS";mtScreen("FICHADAS IMPORTADAS",4);
  android.database.sqlite.SQLiteDatabase r=db.getReadableDatabase();
  Cursor summary=r.rawQuery("SELECT COUNT(*),MIN(substr(stamp,1,10)),MAX(substr(stamp,1,10)),COUNT(DISTINCT person_id) FROM punches",null);
  int total=0,people=0;String first="",last="";
  if(summary.moveToFirst()){total=summary.getInt(0);first=summary.getString(1);last=summary.getString(2);people=summary.getInt(3);}summary.close();
  if(total==0){
   body.addView(mtText("NO HAY FICHADAS GUARDADAS. Importá Attendance logs.xls para verlas aquí.",15,mtPale(),true));
   mtAddLink("⇩","IMPORTAR FICHADAS","Elegir el archivo del reloj",this::pick);
   return;
  }
  body.addView(mtText(total+" MARCACIONES GUARDADAS · "+people+" EMPLEADOS",18,Color.WHITE,true));
  body.addView(mtText("Período: "+first+" al "+last,13,mtPale(),false));
  final String lastDay=last;
  mtAddLink("◷","VER ÚLTIMA FECHA CON DATOS",lastDay+" · detalle del día",()->importedPunchDay(lastDay));
  Cursor days=r.rawQuery("SELECT substr(stamp,1,10) AS d, COUNT(*),COUNT(DISTINCT person_id) FROM punches GROUP BY substr(stamp,1,10) ORDER BY d DESC LIMIT 120",null);
  try{
   while(days.moveToNext()){
    String day=days.getString(0);
    int punches=days.getInt(1),workers=days.getInt(2);
    mtAddLink("▣",day,punches+" marcaciones · "+workers+" empleados",()->importedPunchDay(day));
   }
  }finally{days.close();}
 }
 void importedPunchDay(String day){
  currentScreen="FICHADAS";mtScreen("FICHADAS · "+day,4);
  mtAddLink("‹","VOLVER A LAS FECHAS","Historial importado",this::importedPunchHistory);
  android.database.sqlite.SQLiteDatabase r=db.getReadableDatabase();
  Cursor c=r.rawQuery("SELECT p.id,COALESCE(NULLIF(p.name,''),p.id),COUNT(*),MIN(substr(x.stamp,12,8)),MAX(substr(x.stamp,12,8)) "+
   "FROM punches x JOIN people p ON p.id=x.person_id WHERE substr(x.stamp,1,10)=? GROUP BY p.id,p.name ORDER BY p.name",new String[]{day});
  int shown=0;
  try{
   while(c.moveToNext()){
    String pid=c.getString(0),name=c.getString(1),first=c.getString(3),last=c.getString(4);
    int qty=c.getInt(2);shown++;
    mtAddLink("●",name,qty+" marcaciones · "+first+(qty>1?" → "+last:""),()->importedPunchPersonDay(pid,day));
   }
  }finally{c.close();}
  if(shown==0)body.addView(mtText("Sin marcaciones guardadas para esta fecha.",13,mtPale(),false));
 }
 void importedPunchPersonDay(String pid,String day){
  currentScreen="FICHADAS";mtScreen("FICHADAS DEL EMPLEADO",4);
  mtAddLink("‹","VOLVER AL DÍA",day,()->importedPunchDay(day));
  Cursor c=db.getReadableDatabase().rawQuery("SELECT stamp,COALESCE(device,'') FROM punches WHERE person_id=? AND substr(stamp,1,10)=? ORDER BY stamp",new String[]{pid,day});
  try{
   while(c.moveToNext()){
    String stamp=c.getString(0),device=c.getString(1);
    mtAddLink("◷",stamp.length()>10?stamp.substring(11).replace("T"," "):stamp,"Reloj "+device,()->mtEmployee(pid));
   }
  }finally{c.close();}
 }
'''
s=s.replace(mark,code+"\n"+mark,1)
# Visible navigation from both import hub and the personnel tab.
s=s.replace('mtAddLink("●","REVISAR PERSONAL","Ver empleados y completar datos faltantes",this::mtPersonnel);',
 '''mtAddLink("▣","VER FICHADAS IMPORTADAS","Historial por fecha, persona y horario",this::importedPunchHistory);
  mtAddLink("●","REVISAR PERSONAL","Ver empleados y completar datos faltantes",this::mtPersonnel);''',1)
p.write_text(s)
print("V70 history of real punches by stored date")
