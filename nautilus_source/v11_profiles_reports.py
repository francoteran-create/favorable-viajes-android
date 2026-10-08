from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# Transform profile summary into executive cards
old='body.addView(label(String.format(Locale.US,"PRESENTISMO %.1f%%\\n%d de %d jornadas trabajadas\\nAusencias %d · Tardanzas %d · %d minutos tarde\\nIncidencias %d\\nHoras reloj %.1f · Reconocidas %.1f",pct,pres,exp,abs,late,lateMin,inc,clock/60.0,rec/60.0),17));'
new='''body.addView(premiumCard("PRESENTISMO",String.format(Locale.US,"%.1f%%",pct),pres+" de "+exp+" jornadas trabajadas",pct>=90?Color.rgb(48,205,166):Color.rgb(244,190,46)));body.addView(metricRow("AUSENCIAS",""+abs,"TARDANZAS",""+late,"INCIDENCIAS",""+inc));body.addView(premiumCard("HORAS DEL MES",String.format(Locale.US,"%.1f h",clock/60.0),"Reconocidas "+String.format(Locale.US,"%.1f h",rec/60.0)+" · "+lateMin+" min tarde",Color.rgb(66,185,220)));sectionTitle("ACCIONES","Historial, turnos, incidencias y liquidación");'''
if old in s:s=s.replace(old,new)
# Directory cards: convert generated buttons into richer dark cards with identity/status hierarchy
old2='LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,-2);lp.setMargins(0,5,0,5);body.addView(b,lp);'
new2='''android.graphics.drawable.GradientDrawable cg=new android.graphics.drawable.GradientDrawable();cg.setOrientation(android.graphics.drawable.GradientDrawable.Orientation.LEFT_RIGHT);cg.setColors(new int[]{Color.rgb(13,43,56),Color.rgb(7,25,35)});cg.setCornerRadius(24);cg.setStroke(1,Color.rgb(46,95,111));b.setBackground(cg);b.setPadding(18,16,18,16);LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,-2);lp.setMargins(0,6,0,6);body.addView(b,lp);'''
# only last occurrence in employee directory is acceptable; replace all matching generated profile button layout if present
s=s.replace(old2,new2)
# Reports: executive cover and quick cards if method exists
needle='void reports(){base("INFORMES");sectionTitle("CENTRO DE INFORMES","Presentismo, incidencias, horas y liquidación");'
if needle in s:
 s=s.replace(needle,needle+'body.addView(premiumCard("INFORME MENSUAL","RESUMEN EJECUTIVO","Presentismo · horas · novedades",Color.rgb(244,190,46)));')
# More menu version stamp
needle2='void moreMenu(){base("MÁS");sectionTitle("ADMINISTRACIÓN","Configuración, importación y herramientas del sistema");'
if needle2 in s:s=s.replace(needle2,needle2+'body.addView(statusPill("NAUTILUS PRESENTISMO · V11 DESIGN",Color.rgb(244,190,46)));')
p.write_text(s)
print("V11 profile/report design applied")
