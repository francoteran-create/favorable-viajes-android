from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text(); mark=' void btn(String s,Runnable r){'; assert mark in s
code=r'''
 void quickReportHub(){
  currentScreen="INFORME_RAPIDO";base("INFORME RÁPIDO");body.addView(refHero("INFORME RÁPIDO","Todo Nautilus en uno o dos toques"));sectionTitle("PERÍODO","Resumen + sectores + personal + incidencias");btn("ESTA SEMANA · LUNES A DOMINGO",()->quickReport(false));btn("ESTE MES",()->quickReport(true));btn("INFORMES DETALLADOS",this::exactReports);exactBottom("INFORMES");
 }
 void quickReport(boolean month){
  Calendar now=Calendar.getInstance();Calendar a=(Calendar)now.clone(),b=(Calendar)now.clone();
  if(month){a.set(Calendar.DAY_OF_MONTH,1);b.set(Calendar.DAY_OF_MONTH,b.getActualMaximum(Calendar.DAY_OF_MONTH));}
  else{int d=a.get(Calendar.DAY_OF_WEEK);int delta=(d==Calendar.SUNDAY)?6:d-Calendar.MONDAY;a.add(Calendar.DAY_OF_MONTH,-delta);b=(Calendar)a.clone();b.add(Calendar.DAY_OF_MONTH,6);}
  SimpleDateFormat f=new SimpleDateFormat("yyyy-MM-dd",Locale.US),nice=new SimpleDateFormat("dd/MM",Locale.US);String from=f.format(a.getTime()),to=f.format(b.getTime());
  currentScreen="INFORME_RAPIDO";base(month?"INFORME DEL MES":"INFORME DE LA SEMANA");body.addView(refHero(month?"ESTE MES":"ESTA SEMANA",nice.format(a.getTime())+" — "+nice.format(b.getTime())));
  int scheduled=0,worked=0,abs=0,late=0;Calendar x=(Calendar)a.clone();Calendar today=Calendar.getInstance();today.set(Calendar.HOUR_OF_DAY,23);today.set(Calendar.MINUTE,59);
  while(!x.after(b)){String day=f.format(x.getTime());boolean future=x.after(today);Cursor c=db.getReadableDatabase().rawQuery("SELECT id FROM people WHERE active=1",null);while(c.moveToNext()){DayResult r=calcDay(c.getString(0),day);if(r!=null&&r.expected){scheduled++;if(!future){if(r.worked>0){worked++;if(r.late>0)late++;}else abs++;}}}c.close();x.add(Calendar.DAY_OF_MONTH,1);}
  LinearLayout stats=new LinearLayout(this);stats.setOrientation(LinearLayout.HORIZONTAL);String[] n={""+scheduled,""+worked,""+abs,""+late};String[] t={"DIAGRAMADOS","ASISTENCIAS","AUSENCIAS","TARDANZAS"};int[] co={Color.rgb(55,120,155),Color.rgb(48,205,166),Color.rgb(235,82,82),Color.rgb(244,190,46)};for(int i=0;i<4;i++)stats.addView(exactStat(n[i],t[i],co[i]),new LinearLayout.LayoutParams(0,-2,1));body.addView(stats);
  sectionTitle("DETALLE DEL PERSONAL","Día por día · programado vs. fichado");Cursor pcur=db.getReadableDatabase().rawQuery("SELECT id,name,sector FROM people WHERE active=1 ORDER BY sector,name",null);while(pcur.moveToNext()){String pid=pcur.getString(0),name=pcur.getString(1),sec=pcur.getString(2);int ps=0,pw=0,pa=0,pl=0;Calendar q=(Calendar)a.clone();while(!q.after(b)){String day=f.format(q.getTime());DayResult r=calcDay(pid,day);if(r!=null&&r.expected){ps++;if(!q.after(today)){if(r.worked>0){pw++;if(r.late>0)pl++;}else pa++;}}q.add(Calendar.DAY_OF_MONTH,1);}String sub="Diagramados "+ps+" · Asist. "+pw+" · Aus. "+pa+" · Tard. "+pl;LinearLayout row=employeeDayCard(pid,name,sec,sub,"VER FICHA",Color.rgb(48,205,166));final String fp=pid;row.setOnClickListener(v->exactPersonal(fp));body.addView(row);}pcur.close();
  sectionTitle("EXPORTAR / COMPARTIR","Salida rápida del informe");btn("EXPORTAR CSV / EXCEL",this::exportCsv);btn("GENERAR PDF",this::reports);btn("COMPARTIR",()->shareText("Nautilus Country · "+(month?"Informe mensual ":"Informe semanal ")+from+" a "+to+"\nDiagramados: "+scheduled+" · Asistencias: "+worked+" · Ausencias: "+abs+" · Tardanzas: "+late));exactBottom("INFORMES");
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Make quick report a first-class action in Reports and Home.
needle='void exactReports(){'
# insert visible action immediately after report hero when exactReports body is built
s=s.replace('body.addView(refHero("INFORMES","Nautilus Country Presentismo"));','body.addView(refHero("INFORMES","Nautilus Country Presentismo"));btn("INFORME RÁPIDO · SEMANA / MES",this::quickReportHub);')
# home gets a prominent import + quick report entry without claiming real-time status
s=s.replace('body.addView(referenceRow("✓","OPERACIÓN NORMAL","Todo el personal esperado está cubierto","",Color.rgb(48,205,166)));','body.addView(referenceRow("◈","PLANIFICACIÓN Y CONTROL","Diagrama del día + última información importada","",Color.rgb(48,205,166)));btn("IMPORTAR ARCHIVO DEL RELOJ",()->attendance(new Date()));btn("INFORME RÁPIDO · SEMANA / MES",this::quickReportHub);')
s=s.replace('V39 RUNTIME SCHEMA REPAIR','V40 QUICK REPORT CORE')
p.write_text(s);print("V40 quick report core applied")
