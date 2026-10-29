from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 void exactEmployeeMonth(String pid){
  String[] a=personMaster(pid);String name=a[1],sec=a[2];currentScreen="PERSONAL";base("PERSONAL");body.addView(refHero(name,sec+" · ACTIVO"));exactTabs(new String[]{"Resumen","Historial","Turnos","Incidencias"},2,new Runnable[]{()->exactPersonal(pid),()->monthReport(pid),()->exactEmployeeMonth(pid),()->exactIncidents()});Calendar cal=Calendar.getInstance();sectionTitle("DIAGRAMA DE TURNOS",new SimpleDateFormat("MMMM yyyy",new Locale("es","AR")).format(cal.getTime()));int max=cal.getActualMaximum(Calendar.DAY_OF_MONTH);for(int d=1;d<=max;d++){String day=String.format(Locale.US,"%04d-%02d-%02d",cal.get(Calendar.YEAR),cal.get(Calendar.MONTH)+1,d);DayResult r=calcDay(pid,day);if(r==null)continue;String state=r.expected?(r.worked>0?(r.late>0?"TARDE":"TRABAJÓ"):"TRABAJA"):"FRANCO";int co=!r.expected?Color.rgb(90,120,130):r.worked<=0?Color.rgb(244,190,46):r.late>0?Color.rgb(235,82,82):Color.rgb(48,205,166);LinearLayout row=referenceRow(""+d,new SimpleDateFormat("EEEE",new Locale("es","AR")).format(parseDate(day)),r.expected?"Día programado":"Descanso",state,co);final String fd=day;row.setOnClickListener(v->employeeDayProfile(pid,fd));body.addView(row);}btn("COMPARTIR TURNO / DIAGRAMA",()->shareSchedule(pid));exactBottom("PERSONAL");
 }
 Date parseDate(String x){try{return new SimpleDateFormat("yyyy-MM-dd",Locale.US).parse(x);}catch(Exception e){return new Date();}}
'''
s=s.replace(mark,code+"\n"+mark)
s=s.replace('btn("VER DIAGRAMA",()->employeeSchedule(pid));','btn("VER DIAGRAMA",()->exactEmployeeMonth(pid));')
s=s.replace('()->employeeSchedule(pid),()->incidentsReference()','()->exactEmployeeMonth(pid),()->exactIncidents()')
s=s.replace('V32 DYNAMIC TURNS','V33 EMPLOYEE MONTH')
p.write_text(s)
print("V33 employee month applied")
