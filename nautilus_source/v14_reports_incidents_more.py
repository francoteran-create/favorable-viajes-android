from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 void monthlyReferenceReport(){
  base("INFORME MENSUAL");String ym=new SimpleDateFormat("MMMM yyyy",new Locale("es","AR")).format(new Date());body.addView(kicker(ym));
  int expected=0,present=0,absent=0,late=0;
  Cursor pc=db.getReadableDatabase().rawQuery("SELECT id FROM people WHERE active=1",null);String pref=new SimpleDateFormat("yyyy-MM",Locale.US).format(new Date());
  Calendar cc=Calendar.getInstance();int max=cc.getActualMaximum(Calendar.DAY_OF_MONTH);
  while(pc.moveToNext()){String id=pc.getString(0);for(int d=1;d<=max;d++){DayResult r=calcDay(id,String.format(Locale.US,"%s-%02d",pref,d));if(r==null||!r.expected)continue;expected++;if(r.worked>0)present++;else absent++;if(r.late>0)late++;}}pc.close();
  operationalStats(expected,present,absent,late);double pct=expected==0?0:present*100.0/expected;body.addView(premiumCard("PRESENTISMO",String.format(Locale.US,"%.1f%%",pct),"Consolidado mensual",Color.rgb(66,185,220)));
  sectionTitle("DETALLE POR SECTOR","Previstas · presentes · ausentes · tardanzas");
  Cursor sc=db.getReadableDatabase().rawQuery("SELECT name FROM sectors ORDER BY name",null);while(sc.moveToNext()){String sec=sc.getString(0);addRefRow("◉",sec,"Cobertura y novedades del mes","›",Color.rgb(244,190,46),()->sectorDetail(sec));}sc.close();
  sectionTitle("NOVEDADES","Incidencias que requieren revisión");addRefRow("!","Incidencias pendientes","Ausencias · tardanzas · marcaciones","REVISAR",Color.rgb(235,82,82),this::reviews);
  btn("EXPORTAR EXCEL / CSV",this::exportCsv);btn("GENERAR PDF",this::exportReport);
 }
 void incidentsReference(){
  base("INCIDENCIAS");sectionTitle("FILTROS","Mes actual · todos los sectores");
  Cursor c=db.getReadableDatabase().rawQuery("SELECT p.name,COALESCE(s.name,'Sin sector'),p.id FROM people p LEFT JOIN sectors s ON s.id=p.sector_id WHERE p.active=1 ORDER BY p.name",null);String day=new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(new Date());int shown=0;
  while(c.moveToNext()){String nm=c.getString(0),sec=c.getString(1),id=c.getString(2);DayResult r=calcDay(id,day);if(r==null)continue;String issue=null;if(r.expected&&r.worked<=0)issue="No registró entrada";else if(r.late>0)issue="Llegó tarde ("+r.late+" min)";else if(r.incident)issue="Marcación incompleta";if(issue!=null){shown++;addRefRow("●",nm,issue+" · "+sec,"REVISAR",issue.contains("tarde")?Color.rgb(244,190,46):Color.rgb(235,82,82),this::reviews);}}
  c.close();if(shown==0)body.addView(premiumCard("INCIDENCIAS","SIN PENDIENTES","No se detectaron novedades hoy",Color.rgb(48,205,166)));
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Reports actions routed to reference screens.
s=s.replace('addRefRow("▤","Informe mensual","Presentismo por empleado y sector","›",Color.rgb(244,190,46),this::monthClose);','addRefRow("▤","Informe mensual","Presentismo por empleado y sector","›",Color.rgb(244,190,46),this::monthlyReferenceReport);')
s=s.replace('addRefRow("⚠","Informe de incidencias","Tardanzas, ausencias, marcaciones","›",Color.rgb(244,190,46),this::reviews);','addRefRow("⚠","Informe de incidencias","Tardanzas, ausencias, marcaciones","›",Color.rgb(244,190,46),this::incidentsReference);')
# Add exact-reference export entries where reports starts.
needle='addRefRow("◷","Informe de horas","Trabajadas, extras, por sector","›",Color.rgb(244,190,46),this::payrollSummary);'
if needle in s:s=s.replace(needle,needle+'addRefRow("▧","Exportar a Excel / CSV","Generar archivo para compartir","›",Color.rgb(48,205,166),this::exportCsv);addRefRow("▤","Generar PDF","Informe formal de Nautilus Country","›",Color.rgb(235,82,82),this::exportReport);')
# More menu remaining exact rows
needle2='addRefRow("♜","Cobertura mínima","Definir requerimientos por sector","›",Color.rgb(244,190,46),this::coverageSetup);'
if needle2 in s:s=s.replace(needle2,needle2+'addRefRow("▣","Importar fichadas","Desde Attendance logs.xls","›",Color.rgb(244,190,46),this::pick);addRefRow("↻","Backup / Restaurar","Copia de seguridad de datos","›",Color.rgb(244,190,46),this::backup);addRefRow("⚙","Configuración","Tolerancias, horarios, sistema","›",Color.rgb(244,190,46),this::regimes);addRefRow("i","Acerca de","Nautilus Country Presentismo","›",Color.rgb(244,190,46),()->{});')
p.write_text(s)
print("V14 reports incidents more reference screens applied")
