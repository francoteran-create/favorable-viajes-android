from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){';assert mark in s
code=r'''
 void referenceHome(){
  base("INICIO");
  body.setBackgroundResource(ar.com.nautiluscountry.presentismo.R.drawable.nautilus_home_bg);body.setPadding(12,6,12,18);
  nautilusHomeLogo();
  Button turn=dashboardCard("▣  TURNOS","Personal y diagramación",()->weekPlanner(new Date()));body.addView(turn,new LinearLayout.LayoutParams(-1,126));
  LinearLayout a=new LinearLayout(this);a.setOrientation(LinearLayout.HORIZONTAL);
  Button pe=dashboardCard("●  PERSONAL","Fichas y estadísticas",this::employees);
  Button re=dashboardCard("▥  INFORMES","Reportes y exportación",this::quickReportHub);
  a.addView(pe,new LinearLayout.LayoutParams(0,116,1));a.addView(re,new LinearLayout.LayoutParams(0,116,1));body.addView(a);
  LinearLayout b=new LinearLayout(this);b.setOrientation(LinearLayout.HORIZONTAL);
  Button co=dashboardCard("⚙  CONFIGURACIÓN","Reloj, sectores y horarios",this::exactMoreLive);
  Button im=dashboardCard("⇩  IMPORTAR FICHADAS","Desde reloj biométrico",()->attendance(new Date()));
  b.addView(co,new LinearLayout.LayoutParams(0,116,1));b.addView(im,new LinearLayout.LayoutParams(0,116,1));body.addView(b);
  premiumHomeSummary();
  referenceNav();
 }
 void referenceNav(){
  LinearLayout n=new LinearLayout(this);n.setOrientation(LinearLayout.HORIZONTAL);n.setGravity(Gravity.CENTER);n.setPadding(0,10,0,4);
  n.addView(bottomTab("⌂","INICIO",this::referenceHome),new LinearLayout.LayoutParams(0,82,1));
  n.addView(bottomTab("▣","TURNOS",()->weekPlanner(new Date())),new LinearLayout.LayoutParams(0,82,1));
  n.addView(bottomTab("●","PERSONAL",this::employees),new LinearLayout.LayoutParams(0,82,1));
  n.addView(bottomTab("▥","INFORMES",this::quickReportHub),new LinearLayout.LayoutParams(0,82,1));
  n.addView(bottomTab("⚙","CONFIG.",this::exactMoreLive),new LinearLayout.LayoutParams(0,82,1));body.addView(n);
 }
 void weekPlanner(Date focus){
  base("TURNOS · SEMANA");
  Calendar c=Calendar.getInstance();c.setTime(focus);int dow=c.get(Calendar.DAY_OF_WEEK);int back=(dow+5)%7;c.add(Calendar.DAY_OF_MONTH,-back);
  LinearLayout nav=new LinearLayout(this);nav.setOrientation(LinearLayout.HORIZONTAL);
  Button prev=dashboardCard("‹","Semana anterior",()->{Calendar x=Calendar.getInstance();x.setTime(focus);x.add(Calendar.DAY_OF_MONTH,-7);weekPlanner(x.getTime());});
  Button home=dashboardCard("⌂","INICIO",this::referenceHome);
  Button next=dashboardCard("›","Semana siguiente",()->{Calendar x=Calendar.getInstance();x.setTime(focus);x.add(Calendar.DAY_OF_MONTH,7);weekPlanner(x.getTime());});
  nav.addView(prev,new LinearLayout.LayoutParams(0,72,1));nav.addView(home,new LinearLayout.LayoutParams(0,72,1));nav.addView(next,new LinearLayout.LayoutParams(0,72,1));body.addView(nav);
  SimpleDateFormat df=new SimpleDateFormat("yyyy-MM-dd",Locale.US),shown=new SimpleDateFormat("EEE dd/MM",new Locale("es","AR"));
  for(int k=0;k<7;k++){Date d=c.getTime();String ds=df.format(d);Button day=dashboardCard(shown.format(d).toUpperCase(),"VER PERSONAL DIAGRAMADO",()->exactDayRoster(ds));body.addView(day,new LinearLayout.LayoutParams(-1,82));c.add(Calendar.DAY_OF_MONTH,1);}
  referenceNav();
 }
'''
s=s.replace(mark,code+"\n"+mark)
# The safe launcher and all home routes now use the new functional reference home.
s=s.replace('homeFeature("ENTRAR AL SISTEMA","Abrir panel completo",this::realHome)','homeFeature("ENTRAR AL SISTEMA","Abrir panel completo",this::referenceHome)')
# Make the logo itself always HOME.
s=s.replace('logo.setOnClickListener(v->exactToday());','logo.setOnClickListener(v->referenceHome());')
s=s.replace("V50 REFERENCE HOME","V51 FUNCTIONAL REFERENCE REBUILD")
p.write_text(s);print("V51 functional reference rebuild: home, week calendar, persistent home routes")
