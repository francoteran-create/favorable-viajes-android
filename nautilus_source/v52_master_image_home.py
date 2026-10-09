from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){';assert mark in s
code=r'''
 TextView homeTitle(String t){TextView v=new TextView(this);v.setText(t);v.setTextColor(Color.WHITE);v.setTextSize(19);v.setTypeface(Typeface.DEFAULT,Typeface.BOLD);v.setPadding(8,18,8,10);return v;}
 Button refCard(String icon,String title,String sub,Runnable r){Button b=new Button(this);b.setText(icon+"\n"+title+"\n"+sub+"   ›");b.setAllCaps(false);b.setGravity(Gravity.LEFT|Gravity.CENTER_VERTICAL);b.setTextColor(Color.WHITE);b.setTextSize(16);b.setPadding(22,10,16,10);b.setBackgroundResource(R.drawable.nautilus_glass_card);b.setOnClickListener(v->r.run());return b;}
 void masterImageHome(){
  base("");
  body.setBackgroundResource(R.drawable.nautilus_home_bg);body.setPadding(14,6,14,12);
  nautilusHomeLogo();
  Button turn=refCard("▣","TURNOS","Personal y diagramación",()->weekPlanner(new Date()));body.addView(turn,new LinearLayout.LayoutParams(-1,142));
  LinearLayout one=new LinearLayout(this);one.setOrientation(LinearLayout.HORIZONTAL);
  one.addView(refCard("●","PERSONAL","Fichas y estadísticas",this::employees),new LinearLayout.LayoutParams(0,132,1));
  one.addView(refCard("▥","INFORMES","Reportes y exportación",this::quickReportHub),new LinearLayout.LayoutParams(0,132,1));body.addView(one);
  LinearLayout two=new LinearLayout(this);two.setOrientation(LinearLayout.HORIZONTAL);
  two.addView(refCard("⚙","CONFIGURACIÓN","Reloj, sectores y horarios",this::exactMoreLive),new LinearLayout.LayoutParams(0,132,1));
  two.addView(refCard("⇩","IMPORTAR FICHADAS","Desde reloj biométrico",()->attendance(new Date())),new LinearLayout.LayoutParams(0,132,1));body.addView(two);
  body.addView(homeTitle("RESUMEN DEL MES"));premiumHomeSummary();
  body.addView(homeTitle("SEMANA ACTUAL"));premiumWeekStrip();
  referenceNav();
 }
'''
s=s.replace(mark,code+"\n"+mark)
s=s.replace('homeFeature("ENTRAR AL SISTEMA","Abrir panel completo",this::referenceHome)','homeFeature("ENTRAR AL SISTEMA","Abrir panel completo",this::masterImageHome)')
s=s.replace('logo.setOnClickListener(v->referenceHome());','logo.setOnClickListener(v->masterImageHome());')
# bottom HOME now targets the master image layout
s=s.replace('bottomTab("⌂","INICIO",this::referenceHome)','bottomTab("⌂","INICIO",this::masterImageHome)')
s=s.replace("V51 FUNCTIONAL REFERENCE REBUILD","V52 MASTER IMAGE HOME")
p.write_text(s);print("V52 master-image home composition applied")
