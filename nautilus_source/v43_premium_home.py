from pathlib import Path
import os
root=Path(os.environ["PROJECT"]);p=root/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java";s=p.read_text()
# premium card drawable generated as Android resource
d=root/"app/src/main/res/drawable";d.mkdir(parents=True,exist_ok=True)
(d/"nautilus_glass_card.xml").write_text("""<selector xmlns:android="http://schemas.android.com/apk/res/android"><item android:state_pressed="true"><shape><corners android:radius="22dp"/><gradient android:angle="0" android:startColor="#CC123C52" android:endColor="#E6071723"/><stroke android:width="1dp" android:color="#E6D3A84E"/><padding android:left="16dp" android:top="13dp" android:right="16dp" android:bottom="13dp"/></shape></item><item><shape><corners android:radius="22dp"/><gradient android:angle="0" android:startColor="#B70C2C3D" android:endColor="#E604111C"/><stroke android:width="1dp" android:color="#7849C8F2"/><padding android:left="16dp" android:top="13dp" android:right="16dp" android:bottom="13dp"/></shape></item></selector>""")
mark=' void btn(String s,Runnable r){';assert mark in s
code=r'''
 Button homeFeature(String title,String sub,Runnable run){
  Button b=new Button(this);b.setAllCaps(false);b.setGravity(Gravity.LEFT|Gravity.CENTER_VERTICAL);b.setText(title+"\n"+sub);b.setTextColor(Color.WHITE);b.setTextSize(16);b.setMinHeight(86);b.setPadding(18,10,18,10);b.setBackgroundResource(ar.com.nautiluscountry.presentismo.R.drawable.nautilus_glass_card);b.setOnClickListener(v->run.run());return b;
 }
 void premiumHomeActions(){
  sectionTitle("CENTRO DE CONTROL","Nautilus Country · planificación y presentismo");
  Button turns=homeFeature("TURNOS","Semana y diagramación",this::exactWeekTurns);body.addView(turns,new LinearLayout.LayoutParams(-1,98));
  LinearLayout row=new LinearLayout(this);row.setOrientation(LinearLayout.HORIZONTAL);Button people=homeFeature("PERSONAL","Fichas y estadísticas",this::exactPeople);Button reports=homeFeature("INFORMES","Semana · mes · exportar",this::quickReportHub);LinearLayout.LayoutParams hp=new LinearLayout.LayoutParams(0,94,1);hp.setMargins(0,8,4,0);row.addView(people,hp);LinearLayout.LayoutParams hr=new LinearLayout.LayoutParams(0,94,1);hr.setMargins(4,8,0,0);row.addView(reports,hr);body.addView(row);
  LinearLayout row2=new LinearLayout(this);row2.setOrientation(LinearLayout.HORIZONTAL);Button cfg=homeFeature("CONFIGURACIÓN","Sectores y regímenes",this::exactMoreLive);Button imp=homeFeature("IMPORTAR FICHADAS","Archivo del reloj",()->attendance(new Date()));LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(0,94,1);cp.setMargins(0,8,4,10);row2.addView(cfg,cp);LinearLayout.LayoutParams ip=new LinearLayout.LayoutParams(0,94,1);ip.setMargins(4,8,0,10);row2.addView(imp,ip);body.addView(row2);
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Insert premium actions immediately after skin on exactToday.
s=s.replace('applyNautilusHomeSkin();','applyNautilusHomeSkin();premiumHomeActions();',1)
s=s.replace("V42 NAUTILUS HOME SKIN","V43 PREMIUM HOME")
p.write_text(s);print("V43 premium functional home cards applied")
