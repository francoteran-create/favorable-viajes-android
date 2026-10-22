from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void dualClockHub(){'
assert mark in s
code=r'''
 long[] j80Counts(String pid,String from,String to){
  // programmed, attended, scheduled-with-no-punch, roster rest days, needs review, punches, common minutes, extra proposed minutes
  rsEnsure();long[] n=new long[8];
  Cursor c=db.getReadableDatabase().rawQuery(
   "SELECT work_date,start_time FROM scheduled_shifts WHERE person_id=? AND work_date BETWEEN ? AND ?",
   new String[]{pid,from,to});
  try{while(c.moveToNext()){
   String day=c.getString(0),start=c.getString(1);
   if("FRANCO".equals(start)){n[3]++;continue;}
   n[0]++;
   Cursor v=db.getReadableDatabase().rawQuery("SELECT COUNT(*) FROM punches WHERE person_id=? AND substr(stamp,1,10)=?",new String[]{pid,day});
   if(v.moveToFirst()&&v.getInt(0)==0)n[2]++;
   v.close();
  }}finally{c.close();}
  Cursor punchDays=db.getReadableDatabase().rawQuery(
   "SELECT substr(stamp,1,10) FROM punches WHERE person_id=? AND substr(stamp,1,10) BETWEEN ? AND ? GROUP BY substr(stamp,1,10)",
   new String[]{pid,from,to});
  try{while(punchDays.moveToNext()){
   String date=punchDays.getString(0);n[1]++;
   String[] v=hrDay(pid,date);
   if("—".equals(v[1]))n[4]++;
   else{
    int common=rsMinutes(v[2]),extra=rsMinutes(v[3]);
    if(common>=0)n[6]+=common;
    if(extra>=0)n[7]+=extra;
   }
  }}finally{punchDays.close();}
  Cursor p=db.getReadableDatabase().rawQuery("SELECT COUNT(*) FROM punches WHERE person_id=? AND substr(stamp,1,10) BETWEEN ? AND ?",new String[]{pid,from,to});
  try{if(p.moveToFirst())n[5]=p.getLong(0);}finally{p.close();}
  return n;
 }
 void j80MonthlyTable(String from,String to){
  rsEnsure();
  body.addView(mtText("JORNADAS POR EMPLEADO · "+from.substring(0,7),17,mtGold(),true));
  body.addView(mtText("Programadas / con fichadas / pendientes / francos. Tocá un empleado para su detalle. Las jornadas con fichadas no están automáticamente aprobadas.",11,mtPale(),false));
  long[] grand=new long[8];int workers=0;
  Cursor c=db.getReadableDatabase().rawQuery("SELECT id,COALESCE(NULLIF(name,''),id) FROM people WHERE active=1 ORDER BY name",null);
  try{while(c.moveToNext()){
   String pid=c.getString(0),name=c.getString(1);long[] n=j80Counts(pid,from,to);
   // Todos los empleados activos aparecen, aun sin fichadas ni turnos en el mes.
   workers++;for(int i=0;i<n.length;i++)grand[i]+=n[i];
   LinearLayout box=mtPanel();
   TextView nameView=mtText(name+"  ›",14,Color.WHITE,true);box.addView(nameView);
   box.addView(mtText("PROGRAMADAS  "+n[0]+"     CON FICHADAS  "+n[1],12,0xFF4DE49B,true));
   box.addView(mtText("SIN FICHAR*  "+n[2]+"     FRANCOS  "+n[3]+"     REVISAR  "+n[4],11,mtPale(),false));
   box.addView(mtText("MARCAS  "+n[5]+"     COMUNES  "+hrTime((int)n[6])+"     RECARGO  "+hrTime((int)n[7]),11,mtGold(),false));
   box.setOnClickListener(v->rpEmployee(pid,from,to));
   body.addView(box);
  }}finally{c.close();}
  LinearLayout total=mtPanel();
  total.addView(mtText("TOTAL GENERAL DEL PLANTEL",18,mtGold(),true));
  String[] labels={"EMPLEADOS","JORNADAS PROGRAMADAS","JORNADAS CON FICHADAS","PROGRAMADAS SIN FICHAR*","FRANCOS PROGRAMADOS","JORNADAS A REVISAR","FICHADAS INDIVIDUALES","HORAS COMUNES ESTIMADAS","RECARGOS PROPUESTOS"};
  String[] values={""+workers,""+grand[0],""+grand[1],""+grand[2],""+grand[3],""+grand[4],""+grand[5],hrTime((int)grand[6]),hrTime((int)grand[7])};
  for(int i=0;i<labels.length;i++){
   LinearLayout row=new LinearLayout(this);row.setOrientation(LinearLayout.HORIZONTAL);row.setPadding(0,mtDp(5),0,mtDp(5));
   TextView t=mtText(labels[i],11,mtPale(),false),v=mtText(values[i],16,i==2?0xFF4DE49B:Color.WHITE,true);
   v.setGravity(Gravity.RIGHT|Gravity.CENTER_VERTICAL);
   row.addView(t,new LinearLayout.LayoutParams(0,mtDp(37),3));
   row.addView(v,new LinearLayout.LayoutParams(0,mtDp(37),2));total.addView(row);
  }
  total.addView(mtText("*Sin fichar no significa ausencia confirmada. Se necesita cobertura completa del archivo y revisión. Una jornada con fichadas tampoco confirma una jornada completa. Horas y recargos son estimativos.",11,mtPale(),false));
  body.addView(total);
 }
'''
s=s.replace(mark,code+'\n'+mark,1)
# Immediately after the period selector, show EVERY active employee and the total.
# Follow with the detailed punch section, keeping weekly report behavior unchanged.
needle='''  nav.addView(left,new LinearLayout.LayoutParams(0,mtDp(58),1));nav.addView(middle,new LinearLayout.LayoutParams(0,mtDp(58),2));nav.addView(right,new LinearLayout.LayoutParams(0,mtDp(58),1));body.addView(nav);'''
assert needle in s
s=s.replace(needle,needle+'\n  if(monthly)j80MonthlyTable(from,to);',1)
needle='''  Cursor employees=db.getReadableDatabase().rawQuery(
   "SELECT x.person_id,COALESCE(NULLIF(p.name,''),x.person_id),COUNT(*),COUNT(DISTINCT substr(x.stamp,1,10)) "+'''
assert needle in s
s=s.replace(needle,'''  body.addView(mtText("DETALLE DE FICHADAS POR EMPLEADO",15,mtGold(),true));
'''+needle,1)
# Individual view gets clear day counts before charts.
needle='''  body.addView(mtText(person+" · "+from+" — "+to,17,Color.WHITE,true));'''
assert needle in s
s=s.replace(needle,needle+'''
  long[] j=j80Counts(pid,from,to);
  body.addView(mtText("JORNADAS: "+j[1]+" con fichadas · "+j[0]+" programadas · "+j[3]+" francos · "+j[4]+" a revisar",13,mtGold(),true));
''',1)
p.write_text(s)
print("V80: monthly report per-worker day totals, grand total, hours and individual header")
