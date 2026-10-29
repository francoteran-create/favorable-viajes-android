from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
marker=" void managementSummary(){"
assert marker in s
code=r"""
 void attendanceLegend(){
  TextView v=label("ESTADOS  ● Presente   ● Tarde   ● Ausente   ● Franco",12);
  v.setTextColor(Color.rgb(170,205,215));v.setPadding(4,8,4,8);body.addView(v);
 }
 void alertsPanel(){
  int pending=pendingIncidents();
  TextView a=label(pending==0?"SIN INCIDENCIAS PENDIENTES":"ATENCIÓN · "+pending+" INCIDENCIAS PENDIENTES",16);
  a.setTextColor(pending==0?Color.rgb(56,230,143):Color.rgb(244,190,46));a.setPadding(16,14,16,14);
  android.graphics.drawable.GradientDrawable g=new android.graphics.drawable.GradientDrawable();g.setColor(Color.rgb(10,31,42));g.setCornerRadius(18);g.setStroke(1,pending==0?Color.rgb(56,230,143):Color.rgb(244,190,46));a.setBackground(g);body.addView(a);
 }
"""
s=s.replace(marker,code+"\n"+marker)
s=s.replace('body.addView(muted("Indicadores para gestión · mes actual"));','body.addView(muted("Indicadores para gestión · mes actual"));alertsPanel();attendanceLegend();')
p.write_text(s)
