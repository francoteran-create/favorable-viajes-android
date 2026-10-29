from pathlib import Path
import os
root=Path(os.environ["PROJECT"]);p=root/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java";s=p.read_text()
d=root/"app/src/main/res/drawable";d.mkdir(parents=True,exist_ok=True)
(d/"nautilus_stat_chip.xml").write_text("""<shape xmlns:android="http://schemas.android.com/apk/res/android"><corners android:radius="18dp"/><gradient android:angle="90" android:startColor="#D80A2636" android:endColor="#E804111B"/><stroke android:width="1dp" android:color="#5575D9FF"/><padding android:left="10dp" android:top="10dp" android:right="10dp" android:bottom="10dp"/></shape>""")
mark=' void btn(String s,Runnable r){';assert mark in s
code=r'''
 TextView homeStat(String value,String label){
  TextView v=new TextView(this);v.setText(value+"\n"+label);v.setTextColor(Color.WHITE);v.setTextSize(12);v.setGravity(Gravity.CENTER);v.setBackgroundResource(ar.com.nautiluscountry.presentismo.R.drawable.nautilus_stat_chip);v.setPadding(8,10,8,10);return v;
 }
 int[] homeMonthStats(){
  int scheduled=0,worked=0,late=0,abs=0;Calendar c=Calendar.getInstance();int y=c.get(Calendar.YEAR),m=c.get(Calendar.MONTH)+1,max=c.get(Calendar.DAY_OF_MONTH);for(int day=1;day<=max;day++){String ds=String.format(Locale.US,"%04d-%02d-%02d",y,m,day);Cursor pc=db.getReadableDatabase().rawQuery("SELECT id FROM people WHERE active=1",null);while(pc.moveToNext()){DayResult r=calcDay(pc.getString(0),ds);if(r!=null&&r.expected){scheduled++;if(evaluatedThrough(ds)==1){if(r.worked>0)worked++;else abs++;if(r.late>0)late++;}}}pc.close();}return new int[]{scheduled,worked,late,abs};
 }
 void premiumHomeSummary(){
  int[] st=homeMonthStats();int eval=st[1]+st[3],pct=eval==0?0:(int)Math.round(st[1]*100.0/eval);sectionTitle("RESUMEN DEL MES",new SimpleDateFormat("MMMM yyyy",new Locale("es","AR")).format(new Date()).toUpperCase());LinearLayout stats=new LinearLayout(this);stats.setOrientation(LinearLayout.HORIZONTAL);String[][] vals={{pct+"%","PRESENTISMO"},{""+st[1],"ASISTENCIAS"},{""+st[2],"TARDANZAS"},{""+st[3],"AUSENCIAS"}};for(String[] x:vals){LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,72,1);lp.setMargins(3,0,3,0);stats.addView(homeStat(x[0],x[1]),lp);}body.addView(stats);
  Calendar mon=mondayOf(new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(new Date()));sectionTitle("SEMANA ACTUAL","Lunes a domingo · tocá un día");LinearLayout strip=new LinearLayout(this);strip.setOrientation(LinearLayout.HORIZONTAL);Calendar q=(Calendar)mon.clone();for(int i=0;i<7;i++){final String ds=isoDay(q);String dn=new SimpleDateFormat("EE",new Locale("es","AR")).format(q.getTime()).toUpperCase();TextView day=homeStat(new SimpleDateFormat("dd",Locale.US).format(q.getTime()),dn);day.setOnClickListener(v->exactWeekTurns(ds,ds));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,72,1);lp.setMargins(2,0,2,0);strip.addView(day,lp);q.add(Calendar.DAY_OF_MONTH,1);}body.addView(strip);
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Add summary after premium action block in home only.
s=s.replace('applyNautilusHomeSkin();premiumHomeActions();','applyNautilusHomeSkin();premiumHomeActions();premiumHomeSummary();',1)
s=s.replace("V43.1 PREMIUM HOME FIX","V44 PREMIUM HOME SUMMARY")
p.write_text(s);print("V44 premium month summary + tappable current week implemented")
