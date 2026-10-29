from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text(); mark=' void btn(String s,Runnable r){'; assert mark in s
code=r'''
 String weekAnchor=new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(new Date());
 String selectedTurnDay=weekAnchor;
 int evaluatedThrough(String day){ try{Cursor c=db.getReadableDatabase().rawQuery("SELECT MAX(substr(stamp,1,10)) FROM punches",null);String x=c.moveToFirst()?c.getString(0):null;c.close();return x==null?0:(day.compareTo(x)<=0?1:0);}catch(Exception e){return 0;} }
 Calendar mondayOf(String day){Calendar c=Calendar.getInstance();c.setTime(parseDate(day));int d=c.get(Calendar.DAY_OF_WEEK),delta=d==Calendar.SUNDAY?6:d-Calendar.MONDAY;c.add(Calendar.DAY_OF_MONTH,-delta);return c;}
 String isoDay(Calendar c){return new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(c.getTime());}
 void exactWeekTurns(){ exactWeekTurns(weekAnchor,selectedTurnDay); }
 void exactWeekTurns(String anchor,String selected){
  weekAnchor=anchor;selectedTurnDay=selected;currentScreen="SEMANA";base("TURNOS");Calendar mon=mondayOf(anchor);Calendar sun=(Calendar)mon.clone();sun.add(Calendar.DAY_OF_MONTH,6);SimpleDateFormat dm=new SimpleDateFormat("dd/MM",Locale.US);
  body.addView(refHero("SEMANA",dm.format(mon.getTime())+" — "+dm.format(sun.getTime())));
  LinearLayout nav=new LinearLayout(this);nav.setOrientation(LinearLayout.HORIZONTAL);Button prev=miniBtn("‹ SEMANA");Button today=miniBtn("HOY");Button next=miniBtn("SEMANA ›");prev.setOnClickListener(v->{Calendar z=(Calendar)mon.clone();z.add(Calendar.DAY_OF_MONTH,-7);exactWeekTurns(isoDay(z),isoDay(z));});today.setOnClickListener(v->{String d=new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(new Date());exactWeekTurns(d,d);});next.setOnClickListener(v->{Calendar z=(Calendar)mon.clone();z.add(Calendar.DAY_OF_MONTH,7);exactWeekTurns(isoDay(z),isoDay(z));});nav.addView(prev,new LinearLayout.LayoutParams(0,48,1));nav.addView(today,new LinearLayout.LayoutParams(0,48,1));nav.addView(next,new LinearLayout.LayoutParams(0,48,1));body.addView(nav);
  sectionTitle("SEMANA | MES","Tocá un día para ver el diagrama completo");
  Calendar q=(Calendar)mon.clone();for(int i=0;i<7;i++){final String day=isoDay(q);int exp=0,worked=0,inc=0;Cursor c=db.getReadableDatabase().rawQuery("SELECT id FROM people WHERE active=1",null);while(c.moveToNext()){DayResult r=calcDay(c.getString(0),day);if(r!=null&&r.expected){exp++;if(evaluatedThrough(day)==1&&r.worked>0)worked++;if(evaluatedThrough(day)==1&&(r.worked<=0||r.late>0))inc++;}}c.close();String dow=new SimpleDateFormat("EEEE",new Locale("es","AR")).format(q.getTime()).toUpperCase();String state=evaluatedThrough(day)==0?"PROGRAMADO · FICHADAS PENDIENTES":("Trabajaron "+worked+" · Incidencias "+inc);LinearLayout card=referenceRow(new SimpleDateFormat("dd",Locale.US).format(q.getTime()),dow,exp+" personas diagramadas",state,day.equals(selected)?Color.rgb(244,190,46):Color.rgb(48,205,166));card.setPadding(14,14,14,14);card.setMinimumHeight(86);card.setOnClickListener(v->exactWeekTurns(anchor,day));body.addView(card);q.add(Calendar.DAY_OF_MONTH,1);}
  btn("VER MES",this::exactDynamicTurns);sectionTitle("DIAGRAMA DEL DÍA",selected);
  Cursor pc=db.getReadableDatabase().rawQuery("SELECT id,name,sector FROM people WHERE active=1 ORDER BY sector,name",null);while(pc.moveToNext()){String pid=pc.getString(0),name=pc.getString(1),sec=pc.getString(2);DayResult r=calcDay(pid,selected);if(r==null||!r.expected)continue;String status=evaluatedThrough(selected)==0?"PROGRAMADO · PENDIENTE DE IMPORTAR":(r.worked>0?(r.late>0?"TARDANZA "+r.late+" min":"JORNADA REGISTRADA"):"AUSENCIA / SIN FICHADAS");LinearLayout row=employeeDayCard(pid,name,sec,"Turno programado",status,evaluatedThrough(selected)==0?Color.rgb(244,190,46):(r.worked>0?Color.rgb(48,205,166):Color.rgb(235,82,82)));final String fp=pid;row.setOnClickListener(v->exactPersonal(fp));body.addView(row);}pc.close();exactBottom("TURNOS");
 }
 void shareWorkerShift(String pid,String day){
  String[] a=personMaster(pid);DayResult r=calcDay(pid,day);String state=(r!=null&&r.expected)?"TRABAJA":"FRANCO";String msg="NAUTILUS COUNTRY — DIAGRAMA DE TURNOS\n"+a[1]+" · "+a[2]+"\n"+day+" · "+state;Intent sh=new Intent(Intent.ACTION_SEND);sh.setType("text/plain");sh.putExtra(Intent.EXTRA_TEXT,msg);try{sh.setPackage("com.whatsapp");startActivity(sh);}catch(Exception e){sh.setPackage(null);startActivity(Intent.createChooser(sh,"Enviar turno"));}}
'''
s=s.replace(mark,code+"\n"+mark)
s=s.replace('void exactTurns(){ exactDynamicTurns(); }','void exactTurns(){ exactWeekTurns(); }')
# profile gets direct WhatsApp for today's scheduled status
needle='btn("VER DIAGRAMA",()->exactEmployeeMonth(pid));'
if needle in s:s=s.replace(needle,needle+'btn("ENVIAR TURNO POR WHATSAPP",()->shareWorkerShift(pid,new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(new Date())));')
s=s.replace("V40.2 QUICK REPORT COMPILE FIX","V41 WEEK PLANNING")
p.write_text(s);print("V41 weekly planning + WhatsApp applied")
