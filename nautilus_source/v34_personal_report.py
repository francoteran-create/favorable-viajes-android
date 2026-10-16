from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 int[] employeeMonthNumbers(String pid){
  Calendar cal=Calendar.getInstance();int max=cal.getActualMaximum(Calendar.DAY_OF_MONTH),expected=0,worked=0,absent=0,late=0;for(int d=1;d<=max;d++){String day=String.format(Locale.US,"%04d-%02d-%02d",cal.get(Calendar.YEAR),cal.get(Calendar.MONTH)+1,d);DayResult r=calcDay(pid,day);if(r!=null&&r.expected){expected++;if(r.worked>0)worked++;else absent++;if(r.late>0)late++;}}return new int[]{expected,worked,absent,late};
 }
 void exactEmployeeMetrics(String pid){
  int[] n=employeeMonthNumbers(pid);int pct=n[0]==0?0:(int)Math.round(n[1]*100.0/n[0]);LinearLayout r=new LinearLayout(this);r.setOrientation(LinearLayout.HORIZONTAL);String[][] a={{pct+"%","PRESENTISMO"},{""+n[1],"DÍAS TRABAJADOS"},{""+n[2],"AUSENCIAS"},{""+n[3],"TARDANZAS"}};int[] co={Color.rgb(48,205,166),Color.rgb(60,160,205),Color.rgb(235,82,82),Color.rgb(244,190,46)};for(int i=0;i<4;i++){LinearLayout x=exactStat(a[i][0],a[i][1],co[i]);LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,-2,1);lp.setMargins(3,4,3,4);r.addView(x,lp);}body.addView(r);
 }
 void exactEmployeeReport(String pid){
  String[] a=personMaster(pid);currentScreen="INFORME";base("INFORME INDIVIDUAL");body.addView(refHero(a[1],a[2]+" · "+new SimpleDateFormat("MMMM yyyy",new Locale("es","AR")).format(new Date())));exactEmployeeMetrics(pid);sectionTitle("DATOS PERSONALES","Ficha maestra");body.addView(referenceRow("●","Nombre",a[1],"",Color.rgb(244,190,46)));body.addView(referenceRow("◈","Sector",a[2],"",Color.rgb(48,205,166)));sectionTitle("DETALLE DEL MES","Programación y asistencia");Calendar cal=Calendar.getInstance();int max=cal.getActualMaximum(Calendar.DAY_OF_MONTH);for(int d=1;d<=max;d++){String day=String.format(Locale.US,"%04d-%02d-%02d",cal.get(Calendar.YEAR),cal.get(Calendar.MONTH)+1,d);DayResult r=calcDay(pid,day);if(r==null||!r.expected)continue;String st=r.worked<=0?"AUSENTE":r.late>0?"TARDE "+r.late+" min":"PRESENTE";int co=r.worked<=0?Color.rgb(235,82,82):r.late>0?Color.rgb(244,190,46):Color.rgb(48,205,166);body.addView(referenceRow(""+d,new SimpleDateFormat("EEEE",new Locale("es","AR")).format(parseDate(day)),"Día programado",st,co));}btn("COMPARTIR",()->shareSchedule(pid));btn("EXPORTAR CSV / EXCEL",this::exportCsv);btn("GENERAR PDF",this::reports);exactBottom("INFORMES");
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Personal reference screen metrics become real and adds direct report.
s=s.replace('employeeMetricStrip(pid);','exactEmployeeMetrics(pid);')
s=s.replace('btn("FICHA COMPLETA",()->personnelMasterForm(pid));','btn("FICHA COMPLETA",()->personnelMasterForm(pid));btn("INFORME INDIVIDUAL",()->exactEmployeeReport(pid));')
s=s.replace('V33 EMPLOYEE MONTH','V34 PERSONAL REPORT')
p.write_text(s)
print("V34 personal report applied")
