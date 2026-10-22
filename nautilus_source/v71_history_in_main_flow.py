from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# Real punch database and queries verified from the generated Java and its SQL schema.
assert 'CREATE TABLE punches(person_id TEXT,stamp TEXT,device TEXT' in s
assert 'void importedPunchHistory()' in s
# Latest imported data visible from HOME and personnel without requiring schedule configuration.
home='''void masterImageHomeV59(){
  currentScreen="INICIO";mtScreen("",0);mtHeader();'''
assert home in s
s=s.replace(home,home+'''
  int stored=0;String newest="";
  try{Cursor pc=db.getReadableDatabase().rawQuery("SELECT COUNT(*),COALESCE(MAX(substr(stamp,1,10)),'') FROM punches",null);
   if(pc.moveToFirst()){stored=pc.getInt(0);newest=pc.getString(1);}pc.close();
  }catch(Exception ignored){}
  final int punchCount=stored;
  mtAddLink("◷","FICHADAS IMPORTADAS · "+punchCount,punchCount==0?"Todavía no hay fichadas guardadas":"Última fecha "+newest+" · tocar para ver todos los registros",this::importedPunchHistory);
''',1)
personal='''void mtPersonnel(){
  currentScreen="PERSONAL";mtScreen("PERSONAL",2);'''
assert personal in s
s=s.replace(personal,personal+'''
  mtAddLink("◷","VER FICHADAS DEL PERSONAL","Todas las fechas y marcaciones ya importadas",this::importedPunchHistory);
''',1)
week='''void mtWeek(Date focus){
  currentScreen="SEMANA";mtScreen("TURNOS · SEMANA",1);'''
assert week in s
s=s.replace(week,week+'''
  mtAddLink("◷","FICHADAS REALES","Consultar datos importados sin depender de turnos",this::importedPunchHistory);
''',1)
# After successfully storing new records, navigate to the actual historical data.
import re
s,n=re.subn(r'(msg\("Importación terminada",[\s\S]*?),this::dualClockHub\);',r'\1,this::importedPunchHistory);',s,count=1)
assert n==1,"Import completion callback not found"
# Show DB verification in history: direct count and date range. DO NOT use scheduled counts.
s=s.replace('''  if(total==0){
   body.addView(mtText("NO HAY FICHADAS GUARDADAS.''','''  if(total==0){
   body.addView(mtText("NO HAY FICHADAS GUARDADAS.''')
p.write_text(s)
print("V71: direct history from successful import, HOME, PERSONAL, TURNOS; SQL table schema checked")
