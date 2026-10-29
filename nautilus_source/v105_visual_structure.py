from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 LinearLayout metricRow(String a,String av,String b,String bv,String c,String cv){
  LinearLayout row=new LinearLayout(this);row.setOrientation(LinearLayout.HORIZONTAL);
  miniMetric(row,a,av,Color.rgb(48,205,166));miniMetric(row,b,bv,Color.rgb(244,190,46));miniMetric(row,c,cv,Color.rgb(235,82,82));return row;
 }
 void miniMetric(LinearLayout row,String title,String value,int accent){
  TextView v=label(value+"\n"+title.toUpperCase(Locale.US),14);v.setGravity(Gravity.CENTER);v.setTextColor(Color.WHITE);v.setPadding(8,16,8,16);
  android.graphics.drawable.GradientDrawable g=new android.graphics.drawable.GradientDrawable();g.setColor(Color.rgb(12,36,48));g.setCornerRadius(22);g.setStroke(2,accent);v.setBackground(g);
  LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,-2,1);lp.setMargins(4,4,4,4);row.addView(v,lp);
 }
 TextView statusPill(String t,int color){TextView v=label(t,11);v.setTextColor(color);v.setGravity(Gravity.CENTER);v.setPadding(12,7,12,7);android.graphics.drawable.GradientDrawable g=new android.graphics.drawable.GradientDrawable();g.setColor(Color.rgb(8,28,38));g.setCornerRadius(30);g.setStroke(2,color);v.setBackground(g);return v;}
 void employeeVisualCard(String name,String meta,String state,Runnable open){
  LinearLayout card=new LinearLayout(this);card.setOrientation(LinearLayout.VERTICAL);card.setPadding(18,16,18,16);
  android.graphics.drawable.GradientDrawable g=new android.graphics.drawable.GradientDrawable();g.setColor(Color.rgb(12,35,47));g.setCornerRadius(28);g.setStroke(1,Color.rgb(35,76,92));card.setBackground(g);
  TextView n=label("●  "+name,17);n.setTextColor(Color.WHITE);card.addView(n);TextView m=label(meta,12);m.setTextColor(Color.rgb(155,185,195));card.addView(m);
  int sc=state.contains("TARDE")?Color.rgb(244,190,46):state.contains("AUS")?Color.rgb(235,82,82):Color.rgb(48,205,166);card.addView(statusPill(state,sc));
  card.setOnClickListener(v->open.run());LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,-2);lp.setMargins(0,6,0,6);body.addView(card,lp);
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Add executive visual strip after dashboard status card if known insertion point exists
needle='body.addView(hero);'
if needle in s:
 s=s.replace(needle,needle+'body.addView(metricRow("PRESENTES",""+totalPresent,"TARDE",""+totalLate,"AUSENTES",""+totalAbsent));sectionTitle("COBERTURA","Dotación operativa por sector y turno");',1)
# Calendar header and legend
s=s.replace('void calendarMonth(){base("TURNOS · CALENDARIO");','void calendarMonth(){base("TURNOS");sectionTitle("CALENDARIO OPERATIVO","Trabajo · franco · incidencias · cambios de turno");LinearLayout lg=new LinearLayout(this);lg.setOrientation(LinearLayout.HORIZONTAL);lg.addView(statusPill("TRABAJA",Color.rgb(48,205,166)),new LinearLayout.LayoutParams(0,-2,1));lg.addView(statusPill("FRANCO",Color.rgb(90,160,210)),new LinearLayout.LayoutParams(0,-2,1));lg.addView(statusPill("INCIDENCIA",Color.rgb(235,82,82)),new LinearLayout.LayoutParams(0,-2,1));body.addView(lg);')
# Management summary premium heading
s=s.replace('void managementSummary(){base("GESTIÓN");','void managementSummary(){base("GESTIÓN");sectionTitle("CONTROL DE PERSONAL","Indicadores para gestión, incidencias y liquidación");')
p.write_text(s)
print("V10.5 visual structure applied")
