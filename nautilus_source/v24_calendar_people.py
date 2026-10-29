from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 void dayPeople(String day){
  currentScreen="CALENDARIO";base("DÍA");body.addView(refHero(new SimpleDateFormat("EEEE d 'de' MMMM",new Locale("es","AR")).format(parse(day)),"Personal · horarios · cumplimiento"));
  Cursor c=db.getReadableDatabase().rawQuery("SELECT id,name,sector FROM people WHERE active=1 ORDER BY sector,name",null);
  while(c.moveToNext()){String pid=c.getString(0),name=c.getString(1),sec=c.getString(2);DayResult r=calcDay(pid,day);if(r==null||(!r.expected&&r.worked<=0))continue;
   Cursor q=db.getReadableDatabase().rawQuery("SELECT MIN(ts),MAX(ts) FROM punches WHERE person_id=? AND substr(ts,1,10)=?",new String[]{pid,day});String punches="Sin fichadas";if(q.moveToFirst()&&!q.isNull(0)){String a=q.getString(0),b=q.getString(1);punches="Entrada "+a.substring(11,16)+" · Salida "+b.substring(11,16);}q.close();
   String st=r.worked<=0?"AUSENTE":r.late>0?"TARDE "+r.late+" min":"PRESENTE";int col=r.worked<=0?Color.rgb(235,82,82):r.late>0?Color.rgb(244,190,46):Color.rgb(48,205,166);
   LinearLayout card=referenceRow("●",name,sec+" · "+punches,st,col);final String fp=pid;card.setOnClickListener(v->employeeDayProfile(fp,day));body.addView(card);
  }c.close();
 }
 void employeeDayProfile(String pid,String day){
  currentScreen="PERSONAL";Cursor c=db.getReadableDatabase().rawQuery("SELECT name,sector,regime_id FROM people WHERE id=?",new String[]{pid});if(!c.moveToFirst()){c.close();return;}String name=c.getString(0),sec=c.getString(1),reg=c.getString(2);c.close();base("PERSONAL");body.addView(refHero(name,sec+" · "+reg));body.addView(refChip("ESTE DÍA",Color.rgb(244,190,46)));DayResult r=calcDay(pid,day);String status=r!=null&&r.worked>0?(r.late>0?"LLEGÓ TARDE":"PRESENTE"):"AUSENTE";body.addView(referenceRow("◷","Jornada",day,status,r!=null&&r.worked>0?Color.rgb(48,205,166):Color.rgb(235,82,82)));employeeMetricStrip(pid);
  btn("VER MES / DIAGRAMA",()->employeeSchedule(pid));btn("COMPARTIR TURNO",()->shareSchedule(pid));
 }
 void employeeSchedule(String pid){
  currentScreen="CALENDARIO";Cursor c=db.getReadableDatabase().rawQuery("SELECT name,sector FROM people WHERE id=?",new String[]{pid});String name=pid,sec="";if(c.moveToFirst()){name=c.getString(0);sec=c.getString(1);}c.close();base("DIAGRAMA");body.addView(refHero(name,sec+" · Diagrama mensual"));referenceMonthGrid();sectionTitle("TRABAJA / FRANCO / LICENCIA / INCIDENCIAS");employeeMetricStrip(pid);btn("COMPARTIR TURNO",()->shareSchedule(pid));
 }
 void shareSchedule(String pid){
  Cursor c=db.getReadableDatabase().rawQuery("SELECT name,sector FROM people WHERE id=?",new String[]{pid});String name=pid,sec="";if(c.moveToFirst()){name=c.getString(0);sec=c.getString(1);}c.close();Calendar cal=Calendar.getInstance();String ym=new SimpleDateFormat("yyyy-MM",Locale.US).format(cal.getTime());int max=cal.getActualMaximum(Calendar.DAY_OF_MONTH);StringBuilder b=new StringBuilder("NAUTILUS COUNTRY\nDiagrama de turnos\n"+name+" · "+sec+"\n"+ym+"\n\n");for(int d=1;d<=max;d++){String day=String.format(Locale.US,"%s-%02d",ym,d);DayResult r=calcDay(pid,day);if(r!=null&&r.expected)b.append(String.format(Locale.US,"%02d",d)).append(" · TRABAJA\n");}Intent i=new Intent(Intent.ACTION_SEND);i.setType("text/plain");i.putExtra(Intent.EXTRA_TEXT,b.toString());startActivity(Intent.createChooser(i,"Compartir turno"));
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Calendar days become navigable through a new explicit day picker entry.
# Add calendar-first access on dashboard and turn screen without replacing existing engine.
needle='body.addView(refHero("PRESENTISMO","Control operativo · "+new SimpleDateFormat("EEEE d \'de\' MMMM",new Locale("es","AR")).format(new Date())));'
if needle in s:s=s.replace(needle,needle+'btn("ABRIR ALMANAQUE",this::calendarMonth);',1)
# Add helper day picker in calendar screen; existing grid remains.
calneedle='body.addView(refHero("TURNOS","Calendario de trabajo y francos"));'
if calneedle in s:s=s.replace(calneedle,calneedle+'btn("VER PERSONAL DE HOY",()->dayPeople(new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(new Date())));',1)
s=s.replace('V23 VISUAL FUSION','V24 CALENDAR PEOPLE')
p.write_text(s)
print("V24 calendar-person workflow applied")
