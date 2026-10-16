from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 void statBox(LinearLayout row,String value,String title,int accent){
  LinearLayout box=new LinearLayout(this);box.setOrientation(LinearLayout.VERTICAL);box.setGravity(Gravity.CENTER);box.setPadding(5,13,5,13);
  android.graphics.drawable.GradientDrawable g=new android.graphics.drawable.GradientDrawable();g.setColor(Color.rgb(8,28,39));g.setCornerRadius(18);g.setStroke(1,accent);box.setBackground(g);
  TextView v=label(value,27);v.setTextColor(Color.WHITE);v.setGravity(Gravity.CENTER);box.addView(v);TextView t=label(title,9);t.setTextColor(accent);t.setGravity(Gravity.CENTER);box.addView(t);
  LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,-2,1);lp.setMargins(3,3,3,3);row.addView(box,lp);
 }
 void operationalStats(int expected,int present,int absent,int late){
  LinearLayout row=new LinearLayout(this);row.setOrientation(LinearLayout.HORIZONTAL);
  statBox(row,""+expected,"DEBÍAN TRABAJAR",Color.rgb(120,190,220));statBox(row,""+present,"PRESENTES",Color.rgb(48,205,166));statBox(row,""+absent,"AUSENTE",Color.rgb(235,82,82));statBox(row,""+late,"TARDE",Color.rgb(244,190,46));body.addView(row);
 }
 void sectorDetail(String sector){
  base(sector);sectionTitle("COBERTURA","Personal esperado y estado actual");
  addRefRow("◈",sector,"Cobertura del sector","VER TURNOS",Color.rgb(244,190,46),this::calendarMonth);
  Cursor c=db.getReadableDatabase().rawQuery("SELECT p.id,p.name,COALESCE(r.name,'Sin régimen') FROM people p LEFT JOIN sectors s ON s.id=p.sector_id LEFT JOIN regimes r ON r.id=p.regime_id WHERE p.active=1 AND s.name=? ORDER BY p.name",new String[]{sector});
  String day=new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(new Date());
  while(c.moveToNext()){final String id=c.getString(0);String nm=c.getString(1),reg=c.getString(2);DayResult dr=calcDay(id,day);String state=(dr!=null&&dr.worked>0)?(dr.late>0?"● LLEGÓ TARDE":"● PRESENTE"):"● SIN ENTRADA";int col=state.contains("PRESENTE")?Color.rgb(48,205,166):state.contains("TARDE")?Color.rgb(244,190,46):Color.rgb(235,82,82);addRefRow("●",nm,reg+" · "+state,"›",col,()->employeeProfile(id));}c.close();
 }
 void coverageReference(){
  sectionTitle("COBERTURA POR SECTOR","Estado de dotación esperado para hoy");
  Cursor c=db.getReadableDatabase().rawQuery("SELECT name FROM sectors ORDER BY name",null);
  while(c.moveToNext()){final String sec=c.getString(0);addRefRow("◉",sec,"Personal y turnos","›",Color.rgb(244,190,46),()->sectorDetail(sec));}c.close();
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Dashboard: insert exact four boxes and clickable coverage after hero.
needle='body.addView(hero);'
if needle in s:
 s=s.replace(needle,needle+'operationalStats(totalExpected,totalPresent,totalAbsent,totalLate);coverageReference();',1)
# Employee profile reference tabs and current shift visual.
needle2='TextView h=label(name+"\\n"+sector+" · "+regime,21);'
if needle2 in s:
 s=s.replace(needle2,'body.addView(kicker("RESUMEN     HISTORIAL     TURNOS     INCIDENCIAS"));'+needle2)
needle3='sectionTitle("ACCIONES","Historial, turnos, incidencias y liquidación");'
if needle3 in s:
 s=s.replace(needle3,'body.addView(premiumCard("TURNO ACTUAL",regime,"Sector "+sector,Color.rgb(48,205,166)));sectionTitle("INFORMACIÓN","Sector · régimen · ciclo · tolerancia");'+needle3)
# Calendar: stronger month/card reference.
needle4='sectionTitle("CALENDARIO OPERATIVO","Trabajo · franco · incidencias · cambios de turno");'
if needle4 in s:s=s.replace(needle4,'body.addView(premiumCard("TURNOS","CALENDARIO MENSUAL","Trabajo · franco · licencia · incidencia",Color.rgb(66,185,220)));'+needle4)
p.write_text(s)
print("V13 core reference screens applied")
