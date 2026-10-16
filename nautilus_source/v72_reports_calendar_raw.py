from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
def swap(name, newcode):
 global s
 m=re.search(r'\bvoid\s+'+name+r'\s*\([^)]*\)\s*\{',s)
 assert m,name
 start=s.index('{',m.start());depth=0;quote=None;esc=False
 for i in range(start,len(s)):
  c=s[i]
  if quote:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c==quote:quote=None
   continue
  if c in ['"',"'"]:quote=c;continue
  if c=='{':depth+=1
  elif c=='}':
   depth-=1
   if depth==0:
    s=s[:m.start()]+newcode+s[i+1:]
    return
 raise RuntimeError(name)
code=r'''
 String rpDate(Date date){return new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(date);}
 String rpMonthLabel(Date date){return new SimpleDateFormat("MMMM yyyy",new Locale("es","AR")).format(date).toUpperCase(new Locale("es","AR"));}
 Calendar rpMonth(Date focus){Calendar x=Calendar.getInstance();x.setTime(focus);x.set(Calendar.DAY_OF_MONTH,1);x.set(Calendar.HOUR_OF_DAY,12);return x;}
 String rpMonthKey(Date date){return new SimpleDateFormat("yyyy-MM",Locale.US).format(date);}
 String rpMonthEnd(Date focus){Calendar c=rpMonth(focus);c.set(Calendar.DAY_OF_MONTH,c.getActualMaximum(Calendar.DAY_OF_MONTH));return rpDate(c.getTime());}
 String rpCsvCell(String text){return "\""+(text==null?"":text.replace("\"","\"\""))+"\"";}
 void rpExport(String start,String end,String pid,String label){
  StringBuilder b=new StringBuilder("\uFEFF");
  b.append("NAUTILUS COUNTRY - ").append(label).append("\n");
  b.append("Desde;").append(start).append(";Hasta;").append(end).append("\n");
  b.append("Fecha;Empleado;ID;Primera fichada;Ultima fichada;Marcaciones\n");
  String sql="SELECT substr(x.stamp,1,10),COALESCE(NULLIF(p.name,''),x.person_id),x.person_id,"+
   "MIN(substr(x.stamp,12)),MAX(substr(x.stamp,12)),COUNT(*) FROM punches x "+
   "LEFT JOIN people p ON p.id=x.person_id "+
   "WHERE substr(x.stamp,1,10)>=? AND substr(x.stamp,1,10)<=? "+
   (pid==null?"":"AND x.person_id=? ")+
   "GROUP BY substr(x.stamp,1,10),x.person_id ORDER BY substr(x.stamp,1,10),p.name";
  String[] args=pid==null?new String[]{start,end}:new String[]{start,end,pid};
  Cursor c=db.getReadableDatabase().rawQuery(sql,args);
  try{while(c.moveToNext()){
   for(int k=0;k<6;k++){if(k>0)b.append(';');b.append(rpCsvCell(c.getString(k)));}b.append("\n");
  }}finally{c.close();}
  pendingExport=b.toString();
  Intent intent=new Intent(Intent.ACTION_CREATE_DOCUMENT);
  intent.addCategory(Intent.CATEGORY_OPENABLE);intent.setType("text/csv");
  intent.putExtra(Intent.EXTRA_TITLE,"Nautilus_"+start+"_"+end+(pid==null?"":"_"+pid)+".csv");
  startActivityForResult(intent,SAVE_REPORT);
 }
 void rpPeriod(Date focus,boolean monthly){
  Calendar begin=Calendar.getInstance();begin.setTime(focus);begin.set(Calendar.HOUR_OF_DAY,12);
  Calendar end=(Calendar)begin.clone();
  if(monthly){begin.set(Calendar.DAY_OF_MONTH,1);end.set(Calendar.DAY_OF_MONTH,end.getActualMaximum(Calendar.DAY_OF_MONTH));}
  else{begin.add(Calendar.DAY_OF_MONTH,-((begin.get(Calendar.DAY_OF_WEEK)+5)%7));end=(Calendar)begin.clone();end.add(Calendar.DAY_OF_MONTH,6);}
  String from=rpDate(begin.getTime()),to=rpDate(end.getTime());
  currentScreen="INFORMES";mtScreen(monthly?"INFORME MENSUAL":"INFORME SEMANAL",3);
  LinearLayout nav=new LinearLayout(this);nav.setOrientation(LinearLayout.HORIZONTAL);
  TextView left=mtText("‹ ANTERIOR",12,mtGold(),true);left.setGravity(Gravity.CENTER);
  left.setOnClickListener(v->{Calendar x=(Calendar)begin.clone();x.add(monthly?Calendar.MONTH:Calendar.DAY_OF_MONTH,monthly?-1:-7);rpPeriod(x.getTime(),monthly);});
  TextView middle=mtText(from+"  —  "+to,12,Color.WHITE,true);middle.setGravity(Gravity.CENTER);
  TextView right=mtText("SIGUIENTE ›",12,mtGold(),true);right.setGravity(Gravity.CENTER);
  right.setOnClickListener(v->{Calendar x=(Calendar)begin.clone();x.add(monthly?Calendar.MONTH:Calendar.DAY_OF_MONTH,monthly?1:7);rpPeriod(x.getTime(),monthly);});
  nav.addView(left,new LinearLayout.LayoutParams(0,mtDp(58),1));nav.addView(middle,new LinearLayout.LayoutParams(0,mtDp(58),2));nav.addView(right,new LinearLayout.LayoutParams(0,mtDp(58),1));body.addView(nav);
  Cursor c=db.getReadableDatabase().rawQuery("SELECT COUNT(*),COUNT(DISTINCT person_id),COUNT(DISTINCT substr(stamp,1,10)) FROM punches WHERE substr(stamp,1,10)>=? AND substr(stamp,1,10)<=?",new String[]{from,to});
  int punches=0,people=0,days=0;if(c.moveToFirst()){punches=c.getInt(0);people=c.getInt(1);days=c.getInt(2);}c.close();
  body.addView(mtText(punches+" FICHADAS · "+people+" EMPLEADOS · "+days+" DÍAS CON REGISTROS",15,Color.WHITE,true));
  body.addView(mtText("Datos del reloj. Ausencias y tardanzas sólo se determinan cuando el horario del empleado está configurado; no se inventan.",12,mtPale(),false));
  final String f=from,t=to;final boolean mo=monthly;
  mtAddLink("⇩","GUARDAR INFORME CSV / EXCEL","Elegí carpeta y nombre del archivo",()->rpExport(f,t,null,mo?"INFORME MENSUAL":"INFORME SEMANAL"));
  mtAddLink("▣","VER CALENDARIO","Consultar las fichadas por día",()->mtCalendar(begin.getTime()));
  Cursor employees=db.getReadableDatabase().rawQuery(
   "SELECT x.person_id,COALESCE(NULLIF(p.name,''),x.person_id),COUNT(*),COUNT(DISTINCT substr(x.stamp,1,10)) "+
   "FROM punches x LEFT JOIN people p ON p.id=x.person_id WHERE substr(x.stamp,1,10)>=? AND substr(x.stamp,1,10)<=? "+
   "GROUP BY x.person_id ORDER BY p.name",new String[]{from,to});
  try{
   while(employees.moveToNext()){
    String pid=employees.getString(0),name=employees.getString(1);
    int n=employees.getInt(2),d=employees.getInt(3);
    mtAddLink("●",name,n+" fichadas · "+d+" días registrados",()->rpEmployee(pid,from,to));
   }
  }finally{employees.close();}
  if(punches==0)mtAddLink("◷","SIN FICHADAS EN ESTE PERÍODO","Cambiá de mes o semana con las flechas",this::importedPunchHistory);
 }
 void rpEmployee(String pid,String from,String to){
  currentScreen="INFORMES";mtScreen("INFORME POR EMPLEADO",3);
  Cursor name=db.getReadableDatabase().rawQuery("SELECT COALESCE(NULLIF(name,''),id) FROM people WHERE id=?",new String[]{pid});
  String person=name.moveToFirst()?name.getString(0):pid;name.close();
  body.addView(mtText(person+" · "+from+" — "+to,17,Color.WHITE,true));
  mtAddLink("⇩","GUARDAR INFORME DEL EMPLEADO","Seleccionar carpeta de destino",()->rpExport(from,to,pid,"INFORME POR EMPLEADO"));
  Cursor c=db.getReadableDatabase().rawQuery(
   "SELECT substr(stamp,1,10),COUNT(*),MIN(substr(stamp,12)),MAX(substr(stamp,12)) FROM punches "+
   "WHERE person_id=? AND substr(stamp,1,10)>=? AND substr(stamp,1,10)<=? GROUP BY substr(stamp,1,10) ORDER BY 1 DESC",
   new String[]{pid,from,to});
  try{while(c.moveToNext()){String date=c.getString(0);int n=c.getInt(1);
   mtAddLink("◷",date,n+" fichadas · "+c.getString(2)+" — "+c.getString(3),()->importedPunchPersonDay(pid,date));
  }}finally{c.close();}
 }
'''
mark=" void dualClockHub(){"
assert mark in s
s=s.replace(mark,code+"\n"+mark,1)
calendar=r'''void mtCalendar(Date focus){
  currentScreen="CALENDARIO";mtScreen("TURNOS · CALENDARIO MENSUAL",1);
  Calendar cal=rpMonth(focus);final int year=cal.get(Calendar.YEAR),month=cal.get(Calendar.MONTH);
  String start=rpDate(cal.getTime()),finish=rpMonthEnd(cal.getTime());
  Cursor stats=db.getReadableDatabase().rawQuery("SELECT COUNT(*),COUNT(DISTINCT person_id) FROM punches WHERE substr(stamp,1,10) BETWEEN ? AND ?",new String[]{start,finish});
  int total=0,people=0;if(stats.moveToFirst()){total=stats.getInt(0);people=stats.getInt(1);}stats.close();
  LinearLayout bar=new LinearLayout(this);bar.setOrientation(LinearLayout.HORIZONTAL);
  TextView prev=mtText("‹",29,mtGold(),true);prev.setGravity(Gravity.CENTER);prev.setOnClickListener(v->{Calendar x=(Calendar)cal.clone();x.add(Calendar.MONTH,-1);mtCalendar(x.getTime());});
  TextView heading=mtText(rpMonthLabel(cal.getTime()),16,Color.WHITE,true);heading.setGravity(Gravity.CENTER);
  TextView next=mtText("›",29,mtGold(),true);next.setGravity(Gravity.CENTER);next.setOnClickListener(v->{Calendar x=(Calendar)cal.clone();x.add(Calendar.MONTH,1);mtCalendar(x.getTime());});
  bar.addView(prev,new LinearLayout.LayoutParams(mtDp(54),mtDp(57)));
  bar.addView(heading,new LinearLayout.LayoutParams(0,mtDp(57),1));
  bar.addView(next,new LinearLayout.LayoutParams(mtDp(54),mtDp(57)));body.addView(bar);
  body.addView(mtText(total+" MARCACIONES · "+people+" EMPLEADOS CON FICHADAS",13,mtPale(),true));
  final Date focused=cal.getTime();
  mtAddLink("▥","INFORME DE ESTE MES","Listado y exportación",()->rpPeriod(focused,true));
  String[] labels={"LUN","MAR","MIÉ","JUE","VIE","SÁB","DOM"};
  LinearLayout weekdays=new LinearLayout(this);weekdays.setOrientation(LinearLayout.HORIZONTAL);
  for(String day:labels){TextView d=mtText(day,10,mtGold(),true);d.setGravity(Gravity.CENTER);weekdays.addView(d,new LinearLayout.LayoutParams(0,mtDp(30),1));}body.addView(weekdays);
  int offset=(cal.get(Calendar.DAY_OF_WEEK)+5)%7,max=cal.getActualMaximum(Calendar.DAY_OF_MONTH);
  java.util.HashMap<String,Integer> counts=new java.util.HashMap<>();
  Cursor countsCursor=db.getReadableDatabase().rawQuery("SELECT substr(stamp,1,10),COUNT(*) FROM punches WHERE substr(stamp,1,10) BETWEEN ? AND ? GROUP BY substr(stamp,1,10)",new String[]{start,finish});
  try{while(countsCursor.moveToNext())counts.put(countsCursor.getString(0),countsCursor.getInt(1));}finally{countsCursor.close();}
  for(int week=0;week<6;week++){
   if(week*7-offset>=max)break;
   LinearLayout line=new LinearLayout(this);line.setOrientation(LinearLayout.HORIZONTAL);
   for(int col=0;col<7;col++){
    int day=week*7+col-offset+1;
    LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,mtDp(79),1);
    lp.setMargins(mtDp(2),mtDp(2),mtDp(2),mtDp(2));
    if(day<1||day>max){line.addView(new TextView(this),lp);continue;}
    final String date=String.format(Locale.US,"%04d-%02d-%02d",year,month+1,day);
    final int n=counts.containsKey(date)?counts.get(date):0;
    LinearLayout box=new LinearLayout(this);box.setOrientation(LinearLayout.VERTICAL);box.setGravity(Gravity.CENTER);
    box.setBackground(mtBg(n>0?0xFF12523F:0xFF0A293A,0xFF031423,n>0?0xFF38CC95:0xFF31556B,12));
    TextView num=mtText(""+day,19,Color.WHITE,true);num.setGravity(Gravity.CENTER);
    TextView qty=mtText(n>0?""+n:"—",11,n>0?0xFF54EAAA:mtPale(),true);qty.setGravity(Gravity.CENTER);
    box.addView(num,new LinearLayout.LayoutParams(-1,mtDp(38)));box.addView(qty,new LinearLayout.LayoutParams(-1,mtDp(24)));
    box.setOnClickListener(v->importedPunchDay(date));
    box.setContentDescription(date+" · "+n+" fichadas");line.addView(box,lp);
   }body.addView(line);
  }
  body.addView(mtText("El número inferior indica las fichadas reales. Tocá cada día para ver empleados y horarios.",11,mtPale(),false));
  mtAddLink("◷","VER TODO EL HISTORIAL","Todas las fechas importadas",this::importedPunchHistory);
  mtAddLink("▣","VOLVER A SEMANA","Planificación semanal",()->mtWeek(focus));
 }'''
swap("mtCalendar",calendar)
# In modern reports, replace dead-end current-month-only actions with selectable historical reports.
reports=r'''void mtReports(){
  currentScreen="INFORMES";mtScreen("INFORMES",3);
  mtAddLink("▥","INFORME MENSUAL","Elegí meses anteriores o posteriores",()->rpPeriod(new Date(),true));
  mtAddLink("▣","INFORME SEMANAL","Navegación de semana en semana",()->rpPeriod(new Date(),false));
  mtAddLink("●","INFORMES POR EMPLEADO","Seleccioná mes o semana y después empleado",()->rpPeriod(new Date(),true));
  mtAddLink("◷","FICHADAS IMPORTADAS","Consultar todos los registros históricos",this::importedPunchHistory);
  mtAddLink("▦","CALENDARIO MENSUAL","Fichadas reales por fecha",()->mtCalendar(new Date()));
 }'''
swap("mtReports",reports)
# Summary panel's detail goes to a selectable monthly report instead of a locked current month.
s=s.replace('mtPanelTitle("RESUMEN DEL MES","VER DETALLE  ›",()->quickReport(true))',
            'mtPanelTitle("RESUMEN DEL MES","VER MESES  ›",()->rpPeriod(new Date(),true))')
# Home reports button already points to mtReports; historic quickReportHub links retain legacy workflows.
p.write_text(s)
print("V72: real monthly calendar, reports month/week/person, Android folder/file chooser via CREATE_DOCUMENT")
