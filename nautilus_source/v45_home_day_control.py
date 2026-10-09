from pathlib import Path
import os
root=Path(os.environ["PROJECT"]);p=root/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java";s=p.read_text()
d=root/"app/src/main/res/drawable";d.mkdir(parents=True,exist_ok=True)
(d/"nautilus_import_badge.xml").write_text("""<shape xmlns:android="http://schemas.android.com/apk/res/android"><corners android:radius="16dp"/><gradient android:angle="0" android:startColor="#D9144659" android:endColor="#E4071C28"/><stroke android:width="1dp" android:color="#AAE0B455"/><padding android:left="14dp" android:top="10dp" android:right="14dp" android:bottom="10dp"/></shape>""")
mark=' void btn(String s,Runnable r){';assert mark in s
code=r'''
 String lastPunchDate(){
  try{Cursor c=db.getReadableDatabase().rawQuery("SELECT MAX(substr(stamp,1,10)) FROM punches",null);String x=c.moveToFirst()?c.getString(0):null;c.close();return x==null?"SIN IMPORTACIONES":x;}catch(Exception e){return "SIN IMPORTACIONES";}
 }
 void premiumImportStatus(){
  String last=lastPunchDate();TextView v=new TextView(this);v.setText("ÚLTIMA INFORMACIÓN DEL RELOJ\n"+last+"   ·   TOCAR PARA IMPORTAR");v.setTextColor(Color.WHITE);v.setTextSize(12);v.setGravity(Gravity.CENTER_VERTICAL);v.setBackgroundResource(ar.com.nautiluscountry.presentismo.R.drawable.nautilus_import_badge);v.setPadding(16,10,16,10);v.setOnClickListener(x->attendance(new Date()));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,64);lp.setMargins(0,10,0,10);body.addView(v,lp);
 }
 void premiumDayDiagram(){
  String day=new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(new Date());sectionTitle("DIAGRAMA DEL DÍA",new SimpleDateFormat("EEEE dd 'de' MMMM",new Locale("es","AR")).format(new Date()));int shown=0;Cursor c=db.getReadableDatabase().rawQuery("SELECT id,name,sector FROM people WHERE active=1 ORDER BY sector,name",null);while(c.moveToNext()&&shown<6){String pid=c.getString(0);DayResult r=calcDay(pid,day);if(r==null||!r.expected)continue;String status=evaluatedThrough(day)==0?"PROGRAMADO · PENDIENTE DE IMPORTAR":(r.worked>0?(r.late>0?"TARDANZA "+r.late+" min":"JORNADA REGISTRADA"):"SIN FICHADAS");LinearLayout row=employeeDayCard(pid,c.getString(1),c.getString(2),"Programado hoy",status,evaluatedThrough(day)==0?Color.rgb(224,180,72):(r.worked>0?Color.rgb(50,205,166):Color.rgb(235,82,82)));final String fp=pid;row.setOnClickListener(v->exactPersonal(fp));body.addView(row);shown++;}c.close();if(shown==0){TextView empty=label("No hay personal diagramado para esta fecha.",12);empty.setTextColor(Color.rgb(155,180,190));body.addView(empty);}Button all=homeFeature("VER DIAGRAMA COMPLETO","Abrir semana y personal programado",()->exactWeekTurns(day,day));body.addView(all,new LinearLayout.LayoutParams(-1,82));
 }
'''
s=s.replace(mark,code+"\n"+mark)
s=s.replace('applyNautilusHomeSkin();premiumHomeActions();premiumHomeSummary();','applyNautilusHomeSkin();premiumImportStatus();premiumHomeActions();premiumHomeSummary();premiumDayDiagram();',1)
s=s.replace("V44 PREMIUM HOME SUMMARY","V45 PREMIUM DAY CONTROL")
p.write_text(s);print("V45 import status + real day diagram implemented")
