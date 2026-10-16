from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 void exactBottom(String active){
  LinearLayout n=new LinearLayout(this);n.setOrientation(LinearLayout.HORIZONTAL);n.setGravity(Gravity.CENTER);String[] labs={"HOY","PERSONAL","TURNOS","INFORMES","MÁS"};String[] ico={"⌂","♙","▣","▤","☷"};for(int i=0;i<labs.length;i++){final int k=i;LinearLayout z=new LinearLayout(this);z.setOrientation(LinearLayout.VERTICAL);z.setGravity(Gravity.CENTER);TextView a=label(ico[i],18),b=label(labs[i],8);boolean on=labs[i].equals(active);a.setGravity(Gravity.CENTER);b.setGravity(Gravity.CENTER);a.setTextColor(on?Color.rgb(244,190,46):Color.rgb(150,195,215));b.setTextColor(on?Color.rgb(244,190,46):Color.rgb(150,195,215));z.addView(a);z.addView(b);z.setOnClickListener(v->{if(k==0)exactToday();else if(k==1)employees();else if(k==2)exactTurns();else if(k==3)exactReports();else exactMore();});n.addView(z,new LinearLayout.LayoutParams(0,58,1));}body.addView(n);
 }
 void exactPersonList(){
  currentScreen="PERSONAL";base("PERSONAL");body.addView(refHero("PERSONAL","Empleados de Nautilus Country"));Cursor c=db.getReadableDatabase().rawQuery("SELECT id,name,sector FROM people WHERE active=1 ORDER BY sector,name",null);while(c.moveToNext()){final String id=c.getString(0);String name=c.getString(1),sec=c.getString(2);LinearLayout r=employeeDayCard(id,name,sec,"Ficha · régimen · historial","ACTIVO",Color.rgb(48,205,166));r.setOnClickListener(v->exactPersonal(id));body.addView(r);}c.close();exactBottom("PERSONAL");
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Replace PERSONAL bottom route inside exactBottom after insertion's generated code.
s=s.replace('if(k==0)exactToday();else if(k==1)employees();else if(k==2)exactTurns();','if(k==0)exactToday();else if(k==1)exactPersonList();else if(k==2)exactTurns();')
# append bottom nav to exact screens, using targeted endings
s=s.replace('exactStatsRow();exactCoverage();\n }','exactStatsRow();exactCoverage();exactBottom("HOY");\n }')
s=s.replace('exactTabs(new String[]{"Hoy (4)","Turnos","Calendario"},0,new Runnable[]{()->exactSector(),()->touchCalendar(),()->touchCalendar()});dayPeople(new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(new Date()));\n }','exactTabs(new String[]{"Hoy (4)","Turnos","Calendario"},0,new Runnable[]{()->exactSector(),()->touchCalendar(),()->touchCalendar()});dayPeople(new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(new Date()));exactBottom("HOY");\n }')
# reports and more get fixed nav
s=s.replace('body.addView(referenceRow("▣","Generar PDF","Informe formal de Nautilus Country","›",Color.rgb(235,82,82)));\n }','body.addView(referenceRow("▣","Generar PDF","Informe formal de Nautilus Country","›",Color.rgb(235,82,82)));exactBottom("INFORMES");\n }')
s=s.replace('for(String[] q:x)body.addView(referenceRow(q[0],q[1],q[2],"›",Color.rgb(244,190,46)));\n }','for(String[] q:x)body.addView(referenceRow(q[0],q[1],q[2],"›",Color.rgb(244,190,46)));exactBottom("MÁS");\n }')
s=s.replace('V29 EXACT REFERENCE CONTENT','V30 EXACT NAVIGATION')
p.write_text(s)
print("V30 exact navigation applied")
