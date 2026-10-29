from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# Root cause visible in device captures: dashboardCard/refCard Button text is being lost by inherited button styling.
# Use TextView cards instead of Button so labels remain visible on Samsung/Android 10.
s=s.replace('Button dashboardCard(String title,String sub,Runnable run){\n  Button b=new Button(this);','TextView dashboardCard(String title,String sub,Runnable run){\n  TextView b=new TextView(this);')
s=s.replace('Button refCard(String icon,String title,String sub,Runnable r){Button b=new Button(this);','TextView refCard(String icon,String title,String sub,Runnable r){TextView b=new TextView(this);')
# Fix local declarations where these helpers are consumed.
s=s.replace('Button turn=dashboardCard(', 'TextView turn=dashboardCard(')
s=s.replace('Button p=dashboardCard(', 'TextView p=dashboardCard(').replace('Button inf=dashboardCard(', 'TextView inf=dashboardCard(')
s=s.replace('Button cfg=dashboardCard(', 'TextView cfg=dashboardCard(').replace('Button imp=dashboardCard(', 'TextView imp=dashboardCard(')
s=s.replace('Button prev=dashboardCard(', 'TextView prev=dashboardCard(').replace('Button home=dashboardCard(', 'TextView home=dashboardCard(').replace('Button next=dashboardCard(', 'TextView next=dashboardCard(')
s=s.replace('Button day=dashboardCard(', 'TextView day=dashboardCard(')
s=s.replace('Button turn=refCard(', 'TextView turn=refCard(')
# Remove duplicate in-content navs. Keep only the app's fixed bottom navigation supplied by base().
s=s.replace('  referenceNav();\n }','\n }')
# TURNOS week: replace generic empty styled cards with explicit readable day TextViews.
start=s.find(' void weekPlanner(Date focus){')
if start>=0:
 end=s.find('\n }',start)+3
 repl=r''' void weekPlanner(Date focus){
  base("TURNOS · SEMANA");
  btn("⌂ INICIO",this::masterImageHome);
  Calendar c=Calendar.getInstance();c.setTime(focus);int dow=c.get(Calendar.DAY_OF_WEEK);int back=(dow+5)%7;c.add(Calendar.DAY_OF_MONTH,-back);
  LinearLayout nav=new LinearLayout(this);nav.setOrientation(LinearLayout.HORIZONTAL);
  TextView prev=homeStat("‹","ANTERIOR");prev.setOnClickListener(v->{Calendar x=Calendar.getInstance();x.setTime(focus);x.add(Calendar.DAY_OF_MONTH,-7);weekPlanner(x.getTime());});
  TextView now=homeStat("HOY","SEMANA");now.setOnClickListener(v->weekPlanner(new Date()));
  TextView next=homeStat("›","SIGUIENTE");next.setOnClickListener(v->{Calendar x=Calendar.getInstance();x.setTime(focus);x.add(Calendar.DAY_OF_MONTH,7);weekPlanner(x.getTime());});
  nav.addView(prev,new LinearLayout.LayoutParams(0,76,1));nav.addView(now,new LinearLayout.LayoutParams(0,76,1));nav.addView(next,new LinearLayout.LayoutParams(0,76,1));body.addView(nav);
  SimpleDateFormat iso=new SimpleDateFormat("yyyy-MM-dd",Locale.US),shown=new SimpleDateFormat("EEEE dd/MM",new Locale("es","AR"));
  for(int k=0;k<7;k++){final String ds=iso.format(c.getTime());TextView day=homeStat(shown.format(c.getTime()).toUpperCase(),"VER PERSONAL DIAGRAMADO");day.setGravity(Gravity.LEFT|Gravity.CENTER_VERTICAL);day.setPadding(20,8,12,8);day.setOnClickListener(v->exactDayRoster(ds));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,78);lp.setMargins(0,4,0,4);body.addView(day,lp);c.add(Calendar.DAY_OF_MONTH,1);}
 }'''
 s=s[:start]+repl+s[end:]
s=s.replace("V54 PERSONNEL PHOTO + HOME NAV","V55 READABLE COMPONENTS")
p.write_text(s);print("V55: readable TextView cards, single nav, rebuilt weekly screen")
