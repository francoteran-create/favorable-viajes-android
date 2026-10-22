from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' TextView homeTitle(String t){';assert mark in s
code=r'''
 LinearLayout masterCard(String icon,String title,String sub,Runnable run){
  LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);c.setGravity(Gravity.CENTER_VERTICAL);c.setPadding(18,10,14,10);c.setBackgroundResource(R.drawable.nautilus_glass_card);
  TextView a=new TextView(this);a.setText(icon+"  "+title);a.setTextColor(Color.WHITE);a.setTextSize(17);a.setTypeface(Typeface.DEFAULT,Typeface.BOLD);a.setMaxLines(2);
  TextView b=new TextView(this);b.setText(sub);b.setTextColor(Color.rgb(176,198,209));b.setTextSize(12);b.setMaxLines(2);
  c.addView(a,new LinearLayout.LayoutParams(-1,-2));c.addView(b,new LinearLayout.LayoutParams(-1,-2));c.setOnClickListener(v->run.run());return c;
 }
 void masterNav(){
  LinearLayout nav=new LinearLayout(this);nav.setOrientation(LinearLayout.HORIZONTAL);nav.setPadding(2,2,2,2);nav.setBackgroundColor(Color.rgb(3,13,22));
  String[] ico={"⌂","▣","●","▥","⚙"};String[] lab={"INICIO","TURNOS","PERSONAL","INFORMES","CONFIG."};
  Runnable[] act={this::masterImageHome,()->weekPlanner(new Date()),this::employees,this::quickReportHub,this::exactMoreLive};
  for(int i=0;i<5;i++){LinearLayout cell=new LinearLayout(this);cell.setOrientation(LinearLayout.VERTICAL);cell.setGravity(Gravity.CENTER);TextView x=new TextView(this);x.setText(ico[i]);x.setTextColor(Color.WHITE);x.setTextSize(18);x.setGravity(Gravity.CENTER);TextView y=new TextView(this);y.setText(lab[i]);y.setTextColor(Color.WHITE);y.setTextSize(9);y.setGravity(Gravity.CENTER);cell.addView(x,new LinearLayout.LayoutParams(-1,28));cell.addView(y,new LinearLayout.LayoutParams(-1,22));final int q=i;cell.setOnClickListener(v->act[q].run());nav.addView(cell,new LinearLayout.LayoutParams(0,58,1));}
  ((LinearLayout)((ViewGroup)body.getParent().getParent())).addView(nav,new LinearLayout.LayoutParams(-1,62));
 }
 void masterImageHomeV58(){
  LinearLayout root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setBackgroundResource(R.drawable.nautilus_home_bg);
  ScrollView scroll=new ScrollView(this);scroll.setFillViewport(true);body=new LinearLayout(this);body.setOrientation(LinearLayout.VERTICAL);body.setPadding(10,8,10,10);
  nautilusHomeLogo();
  LinearLayout turn=masterCard("▣","TURNOS","Personal y diagramación",()->weekPlanner(new Date()));body.addView(turn,new LinearLayout.LayoutParams(-1,108));
  LinearLayout r1=new LinearLayout(this);r1.setOrientation(LinearLayout.HORIZONTAL);LinearLayout p=masterCard("●","PERSONAL","Fichas y estadísticas",this::employees);LinearLayout inf=masterCard("▥","INFORMES","Reportes y exportación",this::quickReportHub);LinearLayout.LayoutParams h1=new LinearLayout.LayoutParams(0,96,1);h1.setMargins(0,6,3,0);r1.addView(p,h1);LinearLayout.LayoutParams h2=new LinearLayout.LayoutParams(0,96,1);h2.setMargins(3,6,0,0);r1.addView(inf,h2);body.addView(r1);
  LinearLayout r2=new LinearLayout(this);r2.setOrientation(LinearLayout.HORIZONTAL);LinearLayout cfg=masterCard("⚙","CONFIGURACIÓN","Sectores y horarios",this::exactMoreLive);LinearLayout imp=masterCard("⇩","IMPORTAR FICHADAS","Reloj biométrico",()->attendance(new Date()));LinearLayout.LayoutParams q1=new LinearLayout.LayoutParams(0,96,1);q1.setMargins(0,6,3,0);r2.addView(cfg,q1);LinearLayout.LayoutParams q2=new LinearLayout.LayoutParams(0,96,1);q2.setMargins(3,6,0,0);r2.addView(imp,q2);body.addView(r2);
  body.addView(homeTitle("RESUMEN DEL MES"));premiumHomeSummary();body.addView(homeTitle("SEMANA ACTUAL"));premiumWeekStrip();
  scroll.addView(body,new ScrollView.LayoutParams(-1,-2));root.addView(scroll,new LinearLayout.LayoutParams(-1,0,1));
  LinearLayout nav=new LinearLayout(this);nav.setOrientation(LinearLayout.HORIZONTAL);nav.setBackgroundColor(Color.rgb(3,13,22));
  String[] ni={"⌂","▣","●","▥","⚙"};String[] nl={"INICIO","TURNOS","PERSONAL","INFORMES","CONFIG."};Runnable[] na={this::masterImageHomeV58,()->weekPlanner(new Date()),this::employees,this::quickReportHub,this::exactMoreLive};
  for(int i=0;i<5;i++){LinearLayout cell=new LinearLayout(this);cell.setOrientation(LinearLayout.VERTICAL);cell.setGravity(Gravity.CENTER);TextView x=new TextView(this);x.setText(ni[i]);x.setTextColor(i==0?Color.rgb(219,181,83):Color.WHITE);x.setTextSize(17);x.setGravity(Gravity.CENTER);TextView y=new TextView(this);y.setText(nl[i]);y.setTextColor(i==0?Color.rgb(219,181,83):Color.WHITE);y.setTextSize(9);y.setGravity(Gravity.CENTER);cell.addView(x,new LinearLayout.LayoutParams(-1,27));cell.addView(y,new LinearLayout.LayoutParams(-1,20));final int z=i;cell.setOnClickListener(v->na[z].run());nav.addView(cell,new LinearLayout.LayoutParams(0,58,1));}
  root.addView(nav,new LinearLayout.LayoutParams(-1,62));setContentView(root);
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Route every HOME call to the fully composed V58 home.
s=s.replace('this::masterImageHome','this::masterImageHomeV58')
s=s.replace('masterImageHome();','masterImageHomeV58();')
# undo accidental self-name replacement if produced
s=s.replace('masterImageHomeV58V58','masterImageHomeV58')
p.write_text(s);print("V58 explicit composite menus and visible nav labels")
