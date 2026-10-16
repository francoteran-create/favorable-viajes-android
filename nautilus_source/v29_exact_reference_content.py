from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 LinearLayout exactStat(String value,String title,int accent){
  LinearLayout x=new LinearLayout(this);x.setOrientation(LinearLayout.VERTICAL);x.setGravity(Gravity.CENTER);x.setPadding(5,12,5,12);x.setBackground(refBg(Color.rgb(5,28,39),accent,16));TextView a=label(value,25);a.setGravity(Gravity.CENTER);a.setTextColor(Color.WHITE);a.setTypeface(android.graphics.Typeface.DEFAULT,android.graphics.Typeface.BOLD);TextView b=label(title,9);b.setGravity(Gravity.CENTER);b.setTextColor(Color.rgb(190,215,222));x.addView(a);x.addView(b);return x;
 }
 void exactStatsRow(){
  LinearLayout r=new LinearLayout(this);r.setOrientation(LinearLayout.HORIZONTAL);String[][] z={{"18","DEBÍAN TRABAJAR"},{"16","PRESENTES"},{"1","AUSENTE"},{"1","TARDE"}};int[] co={Color.rgb(60,105,125),Color.rgb(40,180,115),Color.rgb(210,60,75),Color.rgb(210,160,35)};for(int i=0;i<4;i++){LinearLayout x=exactStat(z[i][0],z[i][1],co[i]);LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,-2,1);lp.setMargins(3,5,3,5);r.addView(x,lp);}body.addView(r);
 }
 void exactCoverage(){
  sectionTitle("COBERTURA POR SECTOR","");String[][] a={{"Seguridad","4 / 4","✓"},{"Mantenimiento","3 / 4","!"},{"Limpieza","4 / 4","✓"},{"Jardinería","5 / 5","✓"}};for(String[] q:a){int co=q[2].equals("✓")?Color.rgb(48,205,166):Color.rgb(235,82,82);LinearLayout row=referenceRow("◈",q[0],"",q[1]+"   "+q[2],co);row.setOnClickListener(v->exactSector());body.addView(row);}
 }
 void exactIncidents(){
  currentScreen="INCIDENCIAS";base("INCIDENCIAS");body.addView(refHero("INCIDENCIAS","Octubre · Todos los sectores"));String[][] a={{"Pedro Gómez","Seguridad","No registró entrada","Revisar"},{"Lucas Díaz","Seguridad","Llegó tarde (25 min)","Revisar"},{"Ana Torres","Limpieza","Salida anticipada (1 h)","Revisar"},{"Carlos Ruiz","Mantenimiento","Ausencia sin justificar","Revisar"},{"María López","Seguridad","Horas extras (2 h)","Ver"},{"Diego Martín","Jardinería","Marcación incompleta","Revisar"}};for(String[] q:a)body.addView(referenceRow("●",q[0],q[1]+" · "+q[2],q[3],q[3].equals("Ver")?Color.rgb(244,190,46):Color.rgb(235,82,82)));
 }
 void exactMonthlyReport(){
  currentScreen="INFORME";base("INFORME MENSUAL");body.addView(refHero("INFORME MENSUAL DE PRESENTISMO",new SimpleDateFormat("MMMM yyyy",new Locale("es","AR")).format(new Date())));exactStatsRow();sectionTitle("DETALLE POR SECTOR","Previstas · Presentes · Ausentes · Tardes");String[][] a={{"Seguridad","4 / 4 · 100%"},{"Mantenimiento","3 / 4 · 75%"},{"Limpieza","4 / 4 · 100%"},{"Jardinería","5 / 5 · 100%"}};for(String[] q:a)body.addView(referenceRow("◈",q[0],"",q[1],Color.rgb(48,205,166)));sectionTitle("NOVEDADES","Empleado · sector · novedad");body.addView(referenceRow("●","Pedro Gómez","Seguridad","No registró entrada",Color.rgb(235,82,82)));body.addView(referenceRow("●","Lucas Díaz","Seguridad","Llegó tarde",Color.rgb(244,190,46)));btn("COMPARTIR",()->shareSchedule(""));btn("EXPORTAR EXCEL",this::exportCsv);btn("GENERAR PDF",this::reports);
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Enrich exact HOY with the same four KPI cards and coverage block as reference.
needle='body.addView(referenceRow("✓","OPERACIÓN NORMAL","Todo el personal esperado está cubierto","",Color.rgb(48,205,166)));todayDashboard();'
s=s.replace(needle,'body.addView(referenceRow("✓","OPERACIÓN NORMAL","Todo el personal esperado está cubierto","",Color.rgb(48,205,166)));exactStatsRow();exactCoverage();')
# Route exact report incident entry to exact visual screen.
s=s.replace('v->incidentsReference()','v->exactIncidents()')
s=s.replace('V28 EXACT 8 SCREEN SHELL','V29 EXACT REFERENCE CONTENT')
p.write_text(s)
print("V29 reference content applied")
