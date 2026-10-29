from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
def swap(name,src):
 global s
 m=re.search(r'\bvoid\s+'+name+r'\s*\([^)]*\)\s*\{',s);assert m,name
 st=s.index('{',m.start());depth=0;quote=None;esc=False
 for i in range(st,len(s)):
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
   if depth==0:s=s[:m.start()]+src+s[i+1:];return
 raise RuntimeError(name)
code=r'''
 void rsEnsure(){
  db.getWritableDatabase().execSQL("CREATE TABLE IF NOT EXISTS scheduled_shifts(person_id TEXT NOT NULL,work_date TEXT NOT NULL,start_time TEXT NOT NULL,end_time TEXT NOT NULL,cycle_name TEXT NOT NULL,created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY(person_id,work_date))");
 }
 int rsMinutes(String time){
  try{String[] p=time.split(":");if(p.length!=2)return -1;int h=Integer.parseInt(p[0]),m=Integer.parseInt(p[1]);return h<0||h>23||m<0||m>59?-1:h*60+m;}catch(Exception e){return -1;}
 }
 EditText rsInput(String title,String value){
  body.addView(mtText(title,12,mtPale(),true));
  EditText e=new EditText(this);e.setSingleLine(true);e.setText(value);e.setTextColor(Color.WHITE);e.setHintTextColor(Color.GRAY);
  e.setBackgroundColor(Color.rgb(12,40,54));e.setPadding(14,11,14,11);body.addView(e,new LinearLayout.LayoutParams(-1,mtDp(51)));return e;
 }
 void rsPickPerson(boolean forShifts,String from,String to){
  currentScreen="PERSONAL";mtScreen(forShifts?"ASIGNAR TURNOS · ELEGIR EMPLEADO":"INFORME INDIVIDUAL · ELEGIR EMPLEADO",forShifts?1:3);
  body.addView(mtText("Seleccioná el empleado. También aparecen los empleados sin régimen todavía.",13,mtPale(),false));
  Cursor c=db.getReadableDatabase().rawQuery("SELECT id,COALESCE(NULLIF(name,''),id) FROM people WHERE active=1 ORDER BY name",null);
  int total=0;
  try{while(c.moveToNext()){String id=c.getString(0),name=c.getString(1);total++;
   mtAddLink("●",name,"ID del reloj: "+id,()->{if(forShifts)rsSetup(id);else rpEmployee(id,from,to);});
  }}finally{c.close();}
  if(total==0)body.addView(mtText("Primero importá Attendance Report.xls o Attendance logs.xls para incorporar empleados.",14,mtPale(),false));
 }
 void rsSetup(String pid){
  rsEnsure();currentScreen="TURNOS";mtScreen("ARMAR TURNOS DEL EMPLEADO",1);
  Cursor p=db.getReadableDatabase().rawQuery("SELECT COALESCE(NULLIF(name,''),id) FROM people WHERE id=?",new String[]{pid});
  String person=p.moveToFirst()?p.getString(0):pid;p.close();
  body.addView(mtText(person+" · ID "+pid,19,Color.WHITE,true));
  body.addView(mtText("Elegí desde qué día comienza el ciclo, el régimen y los horarios. Guardar generará el diagrama por día sin modificar las fichadas importadas.",12,mtPale(),false));
  EditText date=rsInput("COMIENZO DEL DIAGRAMA · AAAA-MM-DD",rpDate(new Date()));
  EditText length=rsInput("CANTIDAD DE DÍAS A PROGRAMAR", "31");
  body.addView(mtText("RÉGIMEN",12,mtPale(),true));
  Spinner cycle=new Spinner(this);
  String[] cycles={"5x2 · trabaja 5 / franco 2","4x2 · trabaja 4 / franco 2","6x1 · trabaja 6 / franco 1","TODOS LOS DÍAS · sin francos","MANUAL · por día desde calendario"};
  ArrayAdapter<String> adapter=new ArrayAdapter<>(this,android.R.layout.simple_spinner_dropdown_item,cycles);cycle.setAdapter(adapter);body.addView(cycle);
  EditText start=rsInput("HORA DE ENTRADA (HH:MM)","08:00");
  EditText end=rsInput("HORA DE SALIDA (HH:MM)","16:00");
  body.addView(mtText("En turnos nocturnos la salida puede ser al día siguiente (ejemplo 22:00 a 06:00). Los francos se generan desde la fecha de inicio elegida.",12,mtPale(),false));
  mtAddLink("✓","GUARDAR DIAGRAMA","Confirmar y aplicar al empleado",()->{
   String d=date.getText().toString().trim(),a=start.getText().toString().trim(),b=end.getText().toString().trim();
   int amount=-1;try{amount=Integer.parseInt(length.getText().toString().trim());}catch(Exception ignored){}
   if(!d.matches("\\d{4}-\\d\\d-\\d\\d")||rsMinutes(a)<0||rsMinutes(b)<0||amount<1||amount>366){
    msg("Revisar datos","Fecha AAAA-MM-DD, horarios HH:MM y período de 1 a 366 días.",()->rsSetup(pid));return;
   }
   try{
    Calendar c=Calendar.getInstance();SimpleDateFormat df=new SimpleDateFormat("yyyy-MM-dd",Locale.US);df.setLenient(false);c.setTime(df.parse(d));
    int selected=cycle.getSelectedItemPosition(),on=selected==0?5:selected==1?4:selected==2?6:selected==3?1:0;
    int off=selected==0?2:selected==1?2:selected==2?1:0;
    if(selected==4){mtCalendar(c.getTime());return;}
    String regime=selected==0?"5x2":selected==1?"4x2":selected==2?"6x1":"TODOS";
    SQLiteDatabase w=db.getWritableDatabase();w.beginTransaction();
    try{for(int i=0;i<amount;i++){
      boolean works=(i%(on+off))<on;
      ContentValues v=new ContentValues();v.put("person_id",pid);v.put("work_date",df.format(c.getTime()));
      v.put("start_time",works?a:"FRANCO");v.put("end_time",works?b:"FRANCO");v.put("cycle_name",regime);
      w.insertWithOnConflict("scheduled_shifts",null,v,SQLiteDatabase.CONFLICT_REPLACE);c.add(Calendar.DAY_OF_MONTH,1);
    }w.setTransactionSuccessful();}finally{w.endTransaction();}
    msg("Diagrama guardado",amount+" días programados para "+person+". Las fichadas existentes se conservaron.",()->rsPersonPlan(pid,d));
   }catch(Exception ex){msg("No se pudo programar",ex.getMessage(),()->rsSetup(pid));}
  });
  mtAddLink("▣","VER TURNOS GUARDADOS","Diagrama y edición por fecha",()->rsPersonPlan(pid,rpDate(new Date())));
 }
 void rsPersonPlan(String pid,String focus){
  rsEnsure();currentScreen="TURNOS";mtScreen("DIAGRAMA PERSONAL",1);
  Cursor p=db.getReadableDatabase().rawQuery("SELECT name FROM people WHERE id=?",new String[]{pid});
  String person=p.moveToFirst()?p.getString(0):pid;p.close();
  body.addView(mtText(person+" · "+focus,17,Color.WHITE,true));
  mtAddLink("+","CONFIGURAR / REPROGRAMAR","Elegir régimen y horarios",()->rsSetup(pid));
  final Calendar month=Calendar.getInstance();try{month.setTime(new SimpleDateFormat("yyyy-MM-dd",Locale.US).parse(focus));}catch(Exception ignored){}
  Cursor c=db.getReadableDatabase().rawQuery("SELECT work_date,start_time,end_time,cycle_name FROM scheduled_shifts WHERE person_id=? AND substr(work_date,1,7)=? ORDER BY work_date",new String[]{pid,focus.substring(0,7)});
  try{while(c.moveToNext()){
   String day=c.getString(0),start=c.getString(1),end=c.getString(2),regime=c.getString(3);
   mtAddLink("▣",day,start.equals("FRANCO")?"FRANCO · "+regime:start+" — "+end+" · "+regime,()->rsEditDay(pid,day));
  }}finally{c.close();}
  mtAddLink("◷","FICHADAS DEL MISMO MES","Comparar con lo realmente registrado",()->rpEmployee(pid,focus.substring(0,7)+"-01",rpMonthEnd(month.getTime())));
 }
 void rsEditDay(String pid,String date){
  rsEnsure();currentScreen="TURNOS";mtScreen("EDITAR TURNO · "+date,1);
  EditText start=rsInput("ENTRADA HH:MM (o FRANCO)","08:00");
  EditText end=rsInput("SALIDA HH:MM","16:00");
  mtAddLink("✓","GUARDAR DÍA","Modificar sólo esta fecha",()->{
   String a=start.getText().toString().trim().toUpperCase(Locale.ROOT),b=end.getText().toString().trim();
   if(!a.equals("FRANCO")&&(rsMinutes(a)<0||rsMinutes(b)<0)){msg("Horario inválido","Ingresá HH:MM o FRANCO.",()->rsEditDay(pid,date));return;}
   ContentValues v=new ContentValues();v.put("person_id",pid);v.put("work_date",date);
   v.put("start_time",a);v.put("end_time",a.equals("FRANCO")?"FRANCO":b);v.put("cycle_name","MANUAL");
   db.getWritableDatabase().insertWithOnConflict("scheduled_shifts",null,v,SQLiteDatabase.CONFLICT_REPLACE);
   rsPersonPlan(pid,date);
  });
 }
 String[] rsDailyRow(String pid,String date){
  rsEnsure();
  String planned="SIN PROGRAMAR",plannedEnd="",first="",last="",qty="0";
  Cursor c=db.getReadableDatabase().rawQuery("SELECT start_time,end_time FROM scheduled_shifts WHERE person_id=? AND work_date=?",new String[]{pid,date});
  if(c.moveToFirst()){planned=c.getString(0);plannedEnd=c.getString(1);}c.close();
  c=db.getReadableDatabase().rawQuery("SELECT COUNT(*),COALESCE(MIN(substr(stamp,12,5)),''),COALESCE(MAX(substr(stamp,12,5)),'') FROM punches WHERE person_id=? AND substr(stamp,1,10)=?",new String[]{pid,date});
  if(c.moveToFirst()){qty=c.getString(0);first=c.getString(1);last=c.getString(2);}c.close();
  String state=planned.equals("SIN PROGRAMAR")?"SIN TURNO":planned.equals("FRANCO")?(Integer.parseInt(qty)>0?"FICHÓ EN FRANCO":"FRANCO"):
   Integer.parseInt(qty)==0?"SIN FICHADA":Integer.parseInt(qty)==1?"REVISAR: 1 FICHADA":"REGISTRO COMPLETO*";
  return new String[]{planned.equals("SIN PROGRAMAR")?planned:planned.equals("FRANCO")?"FRANCO":planned+"-"+plannedEnd,
   first,last,qty,state};
 }
 String rsPeriodCsv(String from,String to,String pid){
  rsEnsure();StringBuilder b=new StringBuilder("\uFEFF");
  b.append("NAUTILUS COUNTRY - PRELIQUIDACION / CONTROL DE FICHADAS\n");
  b.append("Desde;").append(from).append(";Hasta;").append(to).append("\n");
  b.append("Empleado;ID;Fecha;Turno programado;Primera marca;Ultima marca;Cantidad;Estado;Amplitud HH:MM;Horas liquidables\n");
  Cursor people=db.getReadableDatabase().rawQuery("SELECT id,COALESCE(NULLIF(name,''),id) FROM people WHERE active=1 "+(pid==null?"":"AND id=? ")+"ORDER BY name",pid==null?null:new String[]{pid});
  try{while(people.moveToNext()){
   String id=people.getString(0),name=people.getString(1);
   Calendar day=Calendar.getInstance();SimpleDateFormat fmt=new SimpleDateFormat("yyyy-MM-dd",Locale.US);
   try{day.setTime(fmt.parse(from));}catch(Exception e){continue;}
   while(fmt.format(day.getTime()).compareTo(to)<=0){
    String date=fmt.format(day.getTime());String[] v=rsDailyRow(id,date);
    // Only show material days; do not invent absences for dates outside known import coverage.
    if(!v[0].equals("SIN PROGRAMAR")||!v[3].equals("0")){
     String span="";if(Integer.parseInt(v[3])>1){int a=rsMinutes(v[1]),z=rsMinutes(v[2]);if(a>=0&&z>=0){int diff=z-a;if(diff<0)diff+=1440;span=String.format(Locale.US,"%02d:%02d",diff/60,diff%60);}}
     String[] cols={name,id,date,v[0],v[1],v[2],v[3],v[4],span,"PENDIENTE DE VALIDACIÓN"};
     for(int k=0;k<cols.length;k++){if(k>0)b.append(';');b.append(rpCsvCell(cols[k]));}b.append("\n");
    }
    day.add(Calendar.DAY_OF_MONTH,1);
   }
  }}finally{people.close();}
  b.append("NOTA;Amplitud no equivale a horas trabajadas ni liquidables. Validar pausas, nocturnidad, francos, incidencias y convenios.\n");
  return b.toString();
 }
 void rsSaveReport(String from,String to,String pid){
  pendingExport=rsPeriodCsv(from,to,pid);
  Intent intent=new Intent(Intent.ACTION_CREATE_DOCUMENT);
  intent.addCategory(Intent.CATEGORY_OPENABLE);intent.setType("text/csv");
  intent.putExtra(Intent.EXTRA_TITLE,"Nautilus_Preliquidacion_"+from+"_"+to+(pid==null?"":"_"+pid)+".csv");
  startActivityForResult(intent,SAVE_REPORT);
 }
 void rsMonthlyTable(String from,String to){
  rsEnsure();
  body.addView(mtText("PLANILLA DE CONTROL PARA PRELIQUIDACIÓN",16,mtGold(),true));
  body.addView(mtText("Turnos y fichadas reales por trabajador. Las horas liquidables se dejan pendientes de validación; no se convierten automáticamente las marcas en salario.",12,mtPale(),false));
  String sql="SELECT p.id,COALESCE(NULLIF(p.name,''),p.id),COUNT(x.stamp),COUNT(DISTINCT substr(x.stamp,1,10)) FROM people p "+
   "LEFT JOIN punches x ON x.person_id=p.id AND substr(x.stamp,1,10) BETWEEN ? AND ? "+
   "WHERE p.active=1 GROUP BY p.id ORDER BY p.name";
  Cursor c=db.getReadableDatabase().rawQuery(sql,new String[]{from,to});
  LinearLayout head=new LinearLayout(this);head.setOrientation(LinearLayout.HORIZONTAL);
  String[] titles={"EMPLEADO","FICH.","DÍAS","TUR.","VER"};
  for(String title:titles){TextView t=mtText(title,10,mtGold(),true);t.setGravity(Gravity.CENTER);
   head.addView(t,new LinearLayout.LayoutParams(0,mtDp(36),title.equals("EMPLEADO")?3:1));}
  body.addView(head);
  int count=0;
  try{while(c.moveToNext()){
   String pid=c.getString(0),name=c.getString(1);int punches=c.getInt(2),days=c.getInt(3);
   Cursor shift=db.getReadableDatabase().rawQuery("SELECT COUNT(*) FROM scheduled_shifts WHERE person_id=? AND work_date BETWEEN ? AND ? AND start_time!='FRANCO'",new String[]{pid,from,to});
   int scheduled=shift.moveToFirst()?shift.getInt(0):0;shift.close();
   if(punches==0&&scheduled==0)continue;
   count++;
   LinearLayout row=new LinearLayout(this);row.setOrientation(LinearLayout.HORIZONTAL);row.setPadding(0,mtDp(5),0,mtDp(5));
   String[] values={name,""+punches,""+days,""+scheduled,"›"};
   for(int i=0;i<values.length;i++){TextView t=mtText(values[i],i==0?12:13,Color.WHITE,i!=0);t.setGravity(i==0?Gravity.START|Gravity.CENTER_VERTICAL:Gravity.CENTER);
    row.addView(t,new LinearLayout.LayoutParams(0,mtDp(58),i==0?3:1));}
   row.setOnClickListener(v->rpEmployee(pid,from,to));body.addView(row);
  }}finally{c.close();}
  if(count==0)body.addView(mtText("Sin fichadas ni turnos en este período.",13,mtPale(),false));
 }
'''
assert ' void dualClockHub(){' in s
s=s.replace(' void dualClockHub(){',code+'\n void dualClockHub(){',1)
# Historical monthly/weekly report now includes employee summary table, not just links.
needle='  final String f=from,t=to;final boolean mo=monthly;'
assert needle in s
s=s.replace(needle,needle+'''
  mtAddLink("●","INFORME DE UNA PERSONA","Primero elegir el empleado",()->rsPickPerson(false,f,t));
  mtAddLink("⇩","GUARDAR PLANILLA DE PRELIQUIDACIÓN","Detalle diario de empleados, turnos, fichadas y controles",()->rsSaveReport(f,t,null));
  rsMonthlyTable(from,to);
''',1)
# Enhanced employee detail: scheduled vs punch alongside each day.
needle='''  body.addView(mtText(person+" · "+from+" — "+to,17,Color.WHITE,true));'''
assert needle in s
s=s.replace(needle,needle+'''
  mtAddLink("▣","ASIGNAR O EDITAR TURNOS","Planificar horarios para este empleado",()->rsSetup(pid));
  mtAddLink("⇩","GUARDAR PLANILLA INDIVIDUAL","Elegir carpeta en el teléfono",()->rsSaveReport(from,to,pid));
  rsEnsure();
  Cursor all=db.getReadableDatabase().rawQuery(
   "SELECT d FROM (SELECT substr(stamp,1,10) AS d FROM punches WHERE person_id=? UNION SELECT work_date AS d FROM scheduled_shifts WHERE person_id=?) WHERE d BETWEEN ? AND ? ORDER BY d",
   new String[]{pid,pid,from,to});
  try{while(all.moveToNext()){String day=all.getString(0);String[] v=rsDailyRow(pid,day);
   mtAddLink("◷",day,v[0]+" · "+v[3]+" fichadas · "+v[1]+" / "+v[2]+" · "+v[4],()->importedPunchPersonDay(pid,day));
  }}finally{all.close();}
''',1)
# Reports individual choice opens personnel picker before selecting period.
s=s.replace('mtAddLink("●","INFORMES POR EMPLEADO","Seleccioná mes o semana y después empleado",()->rpPeriod(new Date(),true));',
'''mtAddLink("●","INFORMES POR EMPLEADO","Seleccioná primero un trabajador",()->rsPickPerson(false,rpDate(rpMonth(new Date()).getTime()),rpMonthEnd(new Date())));''')
# Main turns and personnel entry points
s=s.replace('''void mtWeek(Date focus){
  currentScreen="SEMANA";mtScreen("TURNOS · SEMANA",1);''','''void mtWeek(Date focus){
  currentScreen="SEMANA";mtScreen("TURNOS · SEMANA",1);
  mtAddLink("+","ARMAR / ASIGNAR TURNOS","Elegir empleado, régimen 4x2 / 5x2 y horarios",()->rsPickPerson(true,"",""));''',1)
s=s.replace('''void mtPersonnel(){
  currentScreen="PERSONAL";mtScreen("PERSONAL",2);''','''void mtPersonnel(){
  currentScreen="PERSONAL";mtScreen("PERSONAL",2);
  mtAddLink("+","ASIGNAR TURNOS A EMPLEADO","Asistente guiado de programación",()->rsPickPerson(true,"",""));''',1)
p.write_text(s)
print("V73 shift setup + employee picker + monthly payroll review table and daily CSV")
