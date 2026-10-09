from pathlib import Path
import os
root=Path(os.environ["PROJECT"]);p=root/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java";s=p.read_text()
mark=' void btn(String s,Runnable r){';assert mark in s
code=r'''
 TextView bottomTab(String icon,String title,Runnable run){
  TextView v=new TextView(this);v.setText(icon+"\n"+title);v.setTextColor(Color.rgb(210,228,236));v.setTextSize(10);v.setGravity(Gravity.CENTER);v.setPadding(3,8,3,8);v.setOnClickListener(x->run.run());return v;
 }
 void premiumBottomNav(){
  LinearLayout nav=new LinearLayout(this);nav.setOrientation(LinearLayout.HORIZONTAL);nav.setGravity(Gravity.CENTER);nav.setBackgroundColor(Color.rgb(3,14,23));Object[][] items={{"⌂","INICIO",(Runnable)this::exactToday},{"◫","TURNOS",(Runnable)this::exactWeekTurns},{"●","PERSONAL",(Runnable)this::employees},{"▤","INFORMES",(Runnable)this::quickReportHub},{"⚙","CONFIG.",(Runnable)this::exactMoreLive}};for(Object[] it:items){LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,62,1);nav.addView(bottomTab((String)it[0],(String)it[1],(Runnable)it[2]),lp);}LinearLayout.LayoutParams np=new LinearLayout.LayoutParams(-1,62);np.setMargins(0,18,0,0);body.addView(nav,np);
 }
'''
s=s.replace(mark,code+"\n"+mark)
s=s.replace('premiumHomeSummary();premiumDayDiagram();','premiumHomeSummary();premiumDayDiagram();premiumBottomNav();',1)
s=s.replace("V45 PREMIUM DAY CONTROL","V46 PREMIUM NAV")
p.write_text(s);print("V46 premium bottom navigation implemented")
