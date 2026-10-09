from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 TextView exactTab(String title,boolean active,Runnable action){
  TextView v=label(title,11);v.setGravity(Gravity.CENTER);v.setTextColor(active?Color.WHITE:Color.rgb(155,185,198));v.setTypeface(android.graphics.Typeface.DEFAULT,active?android.graphics.Typeface.BOLD:android.graphics.Typeface.NORMAL);v.setBackground(refBg(active?Color.rgb(8,72,111):Color.rgb(5,27,39),active?Color.rgb(33,164,255):Color.rgb(25,83,108),12));v.setPadding(5,10,5,10);v.setOnClickListener(x->action.run());return v;
 }
 void exactTabs(String[] names,int active,Runnable[] actions){
  LinearLayout r=new LinearLayout(this);r.setOrientation(LinearLayout.HORIZONTAL);for(int i=0;i<names.length;i++){final int k=i;r.addView(exactTab(names[i],i==active,actions[k]),new LinearLayout.LayoutParams(0,-2,1));}body.addView(r);
 }
 void exactToday(){
  currentScreen="HOY";base("HOY");body.addView(refHero("NAUTILUS COUNTRY","P R E S E N T I S M O"));TextView date=label(new SimpleDateFormat("EEEE d 'de' MMMM yyyy",new Locale("es","AR")).format(new Date()),12);date.setGravity(Gravity.CENTER);date.setTextColor(Color.WHITE);body.addView(date);
  body.addView(referenceRow("✓","OPERACIÓN NORMAL","Todo el personal esperado está cubierto","",Color.rgb(48,205,166)));todayDashboard();
 }
 void exactSector(){
  currentScreen="SECTOR";base("SEGURIDAD");body.addView(refHero("SEGURIDAD","Cobertura del sector"));body.addView(referenceRow("◈","Seguridad","Cobertura","4 / 4",Color.rgb(48,205,166)));
  exactTabs(new String[]{"Hoy (4)","Turnos","Calendario"},0,new Runnable[]{()->exactSector(),()->touchCalendar(),()->touchCalendar()});dayPeople(new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(new Date()));
 }
 void exactTurns(){
  currentScreen="CALENDARIO";base("TURNOS");body.addView(refHero("TURNOS","Seguridad"));touchCalendar();
 }
 void exactPersonal(String pid){
  currentScreen="PERSONAL";String[] a=personMaster(pid);base("PERSONAL");body.addView(refHero(a[0].isEmpty()?"Empleado":a[0],a[1].isEmpty()?"Sector pendiente":a[1]+" · ACTIVO"));
  exactTabs(new String[]{"Resumen","Historial","Turnos","Incidencias"},0,new Runnable[]{()->exactPersonal(pid),()->monthReport(pid),()->employeeSchedule(pid),()->incidentsReference()});employeeMetricStrip(pid);sectionTitle("TURNO ACTUAL","Horario, entrada y estado");btn("FICHA COMPLETA",()->personnelMasterForm(pid));btn("VER DIAGRAMA",()->employeeSchedule(pid));
 }
 void exactReports(){
  currentScreen="INFORMES";base("INFORMES");body.addView(refHero("INFORMES","Nautilus Country Presentismo"));
  body.addView(referenceRow("▣","Informe mensual","Presentismo por empleado y sector","›",Color.rgb(244,190,46)));body.getChildAt(body.getChildCount()-1).setOnClickListener(v->chooseMonth());
  body.addView(referenceRow("⚠","Informe de incidencias","Tardanzas, ausencias, marcaciones","›",Color.rgb(244,190,46)));body.getChildAt(body.getChildCount()-1).setOnClickListener(v->incidentsReference());
  body.addView(referenceRow("◷","Informe de horas","Trabajadas, extras, por sector","›",Color.rgb(244,190,46)));body.addView(referenceRow("▤","Exportar a Excel / CSV","Generar archivo para compartir","›",Color.rgb(48,205,166)));body.addView(referenceRow("▣","Generar PDF","Informe formal de Nautilus Country","›",Color.rgb(235,82,82)));
 }
 void exactMore(){
  currentScreen="MAS";base("MÁS");body.addView(refHero("MÁS OPCIONES","Configuración y administración"));
  String[][] x={{"♟","Empleados","Gestionar personal"},{"⚙","Sectores","Configurar sectores"},{"◉","Regímenes de turno","4x2, 2x2, 5x2, etc."},{"♜","Cobertura mínima","Definir requerimientos por sector"},{"▣","Importar fichadas","Desde Attendance logs.xls"},{"↻","Backup / Restaurar","Copia de seguridad de datos"},{"⚙","Configuración","Tolerancias, horarios, sistema"},{"●","Acerca de","Nautilus Country"}};
  for(String[] q:x)body.addView(referenceRow(q[0],q[1],q[2],"›",Color.rgb(244,190,46)));
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Route the primary dashboard to the exact 8-screen shell.
# Preserve original functions underneath; exactToday is the new visual entry.
s=s.replace('home();','exactToday();',1)
s=s.replace('V27.1 STARTUP HOTFIX','V28 EXACT 8 SCREEN SHELL')
p.write_text(s)
print("V28 exact eight-screen structural shell applied")
