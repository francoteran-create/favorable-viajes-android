from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
marker=" void sectorStats(){"
assert marker in s
code=r"""
 void employeeProfile(String pid){
  base("FICHA DEL TRABAJADOR");
  Cursor c=db.getReadableDatabase().rawQuery("SELECT p.name,COALESCE(s.name,'Sin sector'),COALESCE(r.name,'Sin régimen') FROM people p LEFT JOIN sectors s ON s.id=p.sector_id LEFT JOIN regimes r ON r.id=p.regime_id WHERE p.id=?",new String[]{pid});
  if(!c.moveToFirst()){c.close();body.addView(label("Empleado no encontrado",16));return;}
  String name=c.getString(0),sector=c.getString(1),regime=c.getString(2);c.close();
  String ym=new SimpleDateFormat("yyyy-MM",Locale.US).format(new Date());
  int exp=0,pres=0,abs=0,late=0,lateMin=0,inc=0,clock=0,rec=0;
  try{
   Calendar cal=Calendar.getInstance();cal.setTime(new SimpleDateFormat("yyyy-MM-dd",Locale.US).parse(ym+"-01"));
   int max=cal.getActualMaximum(Calendar.DAY_OF_MONTH);
   for(int d=1;d<=max;d++){
    DayResult r=dayResult(pid,String.format(Locale.US,"%s-%02d",ym,d));
    if(r==null||!r.expected)continue;
    exp++;if(r.present)pres++;else abs++;
    if(r.lateMinutes>0){late++;lateMin+=r.lateMinutes;}
    if(r.incident)inc++;
    clock+=Math.max(0,r.clockMinutes);rec+=Math.max(0,r.recognizedMinutes);
   }
  }catch(Exception ignored){}
  double pct=exp==0?0:pres*100.0/exp;
  TextView h=label(name+"\n"+sector+" · "+regime,21);h.setTextColor(Color.WHITE);h.setPadding(18,18,18,18);
  android.graphics.drawable.GradientDrawable g=new android.graphics.drawable.GradientDrawable();g.setColor(Color.rgb(8,38,51));g.setCornerRadius(24);g.setStroke(2,Color.rgb(244,190,46));h.setBackground(g);body.addView(h);
  body.addView(label(String.format(Locale.US,"PRESENTISMO %.1f%%\n%d de %d jornadas trabajadas\nAusencias %d · Tardanzas %d · %d minutos tarde\nIncidencias %d\nHoras reloj %.1f · Reconocidas %.1f",pct,pres,exp,abs,late,lateMin,inc,clock/60.0,rec/60.0),17));
  btn("TURNOS / CALENDARIO",this::calendarMonth);btn("INCIDENCIAS",this::reviews);btn("DIAGNÓSTICO",this::diagnosticPicker);btn("LIQUIDACIÓN",this::payrollSummary);
 }
 void employeeDirectory(){
  base("PERSONAL");btn("ESTADÍSTICAS · PERSONAL Y SECTORES",this::statsHub);
  Cursor c=db.getReadableDatabase().rawQuery("SELECT p.id,p.name,COALESCE(s.name,'Sin sector'),COALESCE(r.name,'Sin régimen') FROM people p LEFT JOIN sectors s ON s.id=p.sector_id LEFT JOIN regimes r ON r.id=p.regime_id WHERE p.active=1 ORDER BY s.name,p.name",null);
  while(c.moveToNext()){
   final String id=c.getString(0);Button b=new Button(this);b.setText(c.getString(1)+"\n"+c.getString(2)+" · "+c.getString(3)+"   >");b.setAllCaps(false);b.setGravity(Gravity.LEFT|Gravity.CENTER_VERTICAL);b.setTextColor(Color.WHITE);b.setTextSize(15);
   android.graphics.drawable.GradientDrawable g=new android.graphics.drawable.GradientDrawable();g.setColor(Color.rgb(10,31,42));g.setCornerRadius(18);g.setStroke(1,Color.rgb(33,104,132));b.setBackground(g);b.setOnClickListener(v->employeeProfile(id));
   LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,-2);lp.setMargins(0,5,0,5);body.addView(b,lp);
  }c.close();
 }
"""
s=s.replace(marker,code+"\n"+marker)
s=s.replace('nav(n,"♙\\nPERSONAL",this::employees);','nav(n,"♙\\nPERSONAL",this::employeeDirectory);')
s=s.replace('btn("EMPLEADOS",this::employees);','btn("EMPLEADOS / FICHAS",this::employeeDirectory);')
p.write_text(s)
