from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){';assert mark in s
code=r'''
 Button dashboardCard(String title,String sub,Runnable run){
  Button b=new Button(this);b.setText(title+"\n"+sub+"   ›");b.setAllCaps(false);b.setGravity(Gravity.LEFT|Gravity.CENTER_VERTICAL);b.setTextColor(Color.WHITE);b.setTextSize(17);b.setPadding(24,12,20,12);b.setBackgroundResource(ar.com.nautiluscountry.presentismo.R.drawable.nautilus_glass_card);b.setOnClickListener(v->run.run());return b;
 }
 void realHome(){
  base("INICIO");
  body.setBackgroundResource(ar.com.nautiluscountry.presentismo.R.drawable.nautilus_home_bg);body.setPadding(14,8,14,20);
  nautilusHomeLogo();
  Button turn=dashboardCard("TURNOS","Personal y diagramación",this::exactWeekTurns);body.addView(turn,new LinearLayout.LayoutParams(-1,118));
  LinearLayout r1=new LinearLayout(this);r1.setOrientation(LinearLayout.HORIZONTAL);Button p=dashboardCard("PERSONAL","Fichas y estadísticas",this::employees);Button inf=dashboardCard("INFORMES","Reportes y exportación",this::quickReportHub);r1.addView(p,new LinearLayout.LayoutParams(0,110,1));r1.addView(inf,new LinearLayout.LayoutParams(0,110,1));body.addView(r1);
  LinearLayout r2=new LinearLayout(this);r2.setOrientation(LinearLayout.HORIZONTAL);Button cfg=dashboardCard("CONFIGURACIÓN","Reloj, sectores y horarios",this::exactMoreLive);Button imp=dashboardCard("IMPORTAR FICHADAS","Desde reloj biométrico",()->attendance(new Date()));r2.addView(cfg,new LinearLayout.LayoutParams(0,110,1));r2.addView(imp,new LinearLayout.LayoutParams(0,110,1));body.addView(r2);
  premiumHomeSummary();
  premiumBottomNav();
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Safe boot's ENTER now opens the deliberately simple reference-shaped dashboard.
s=s.replace('homeFeature("ENTRAR AL SISTEMA","Abrir panel completo",this::exactToday)','homeFeature("ENTRAR AL SISTEMA","Abrir panel completo",this::realHome)')
s=s.replace("V49 SAFE BOOT DIAGNOSTIC","V50 REFERENCE HOME")
p.write_text(s);print("V50 reference-shaped functional home implemented")
