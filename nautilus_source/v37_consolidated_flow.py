from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text(); mark=' void btn(String s,Runnable r){'; assert mark in s
code=r'''
 void exactDayRoster(String day){
  currentScreen="DIA";base("DÍA");body.addView(refHero("PERSONAL PROGRAMADO",day));sectionTitle("DEBÍAN TRABAJAR","Según el diagrama cargado");int n=0;Cursor c=db.getReadableDatabase().rawQuery("SELECT id,name,sector FROM people WHERE active=1 ORDER BY sector,name",null);while(c.moveToNext()){String id=c.getString(0),name=c.getString(1),sec=sectorForDate(id,day);DayResult r=calcDay(id,day);if(r==null||!r.expected)continue;n++;String st=r.worked<=0?"AUSENTE / SIN FICHADA":r.late>0?"TARDE "+r.late+" min":"PRESENTE";int co=r.worked<=0?Color.rgb(235,82,82):r.late>0?Color.rgb(244,190,46):Color.rgb(48,205,166);LinearLayout row=employeeDayCard(id,name,sec,"Programado para trabajar",st,co);final String fid=id;row.setOnClickListener(v->employeeDayProfile(fid,day));body.addView(row);}c.close();if(n==0)body.addView(referenceRow("○","SIN PERSONAL PROGRAMADO","No hay empleados previstos para esta fecha","",Color.rgb(90,120,130)));exactBottom("TURNOS");
 }
'''
s=s.replace(mark,code+"\n"+mark)
# All new calendar day taps use the consolidated day roster.
s=s.replace('cell.setOnClickListener(v->dayPeople(day));','cell.setOnClickListener(v->exactDayRoster(day));')
# Exact sector no longer invokes legacy full-screen dayPeople.
old='exactTabs(new String[]{"Hoy (4)","Turnos","Calendario"},0,new Runnable[]{()->exactSector(),()->touchCalendar(),()->touchCalendar()});dayPeople(new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(new Date()));exactBottom("HOY");'
new='exactTabs(new String[]{"Hoy (4)","Turnos","Calendario"},0,new Runnable[]{()->exactSector(),()->exactDynamicTurns(),()->exactDynamicTurns()});btn("VER PERSONAL PROGRAMADO DE HOY",()->exactDayRoster(new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(new Date())));exactBottom("HOY");'
s=s.replace(old,new)
s=s.replace('V36.1 MORE ACTIONS HOTFIX','V37 CONSOLIDATED FLOW')
p.write_text(s);print("V37 consolidated flow applied")
