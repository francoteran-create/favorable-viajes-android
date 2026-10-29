from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 void exactDynamicTurns(){
  currentScreen="CALENDARIO";base("TURNOS");Calendar cal=Calendar.getInstance();String month=new SimpleDateFormat("MMMM yyyy",new Locale("es","AR")).format(cal.getTime());body.addView(refHero("TURNOS",month));sectionTitle("DIAGRAMA MENSUAL","Tocá un día para ver el personal programado");
  LinearLayout week=new LinearLayout(this);week.setOrientation(LinearLayout.HORIZONTAL);for(String x:new String[]{"L","M","X","J","V","S","D"}){TextView v=label(x,10);v.setGravity(Gravity.CENTER);v.setTextColor(Color.rgb(244,190,46));week.addView(v,new LinearLayout.LayoutParams(0,32,1));}body.addView(week);
  Calendar first=(Calendar)cal.clone();first.set(Calendar.DAY_OF_MONTH,1);int offset=(first.get(Calendar.DAY_OF_WEEK)+5)%7,max=cal.getActualMaximum(Calendar.DAY_OF_MONTH),d=1;
  for(int rr=0;rr<6&&d<=max;rr++){LinearLayout line=new LinearLayout(this);line.setOrientation(LinearLayout.HORIZONTAL);for(int col=0;col<7;col++){if((rr==0&&col<offset)||d>max){line.addView(new TextView(this),new LinearLayout.LayoutParams(0,58,1));continue;}final int dd=d++;String day=String.format(Locale.US,"%04d-%02d-%02d",cal.get(Calendar.YEAR),cal.get(Calendar.MONTH)+1,dd);int exp=0,pre=0,inc=0;Cursor c=db.getReadableDatabase().rawQuery("SELECT id FROM people WHERE active=1",null);while(c.moveToNext()){DayResult r=calcDay(c.getString(0),day);if(r!=null&&r.expected){exp++;if(r.worked>0)pre++;if(r.worked<=0||r.late>0)inc++;}}c.close();int border=inc>0?Color.rgb(235,82,82):exp>0?Color.rgb(48,205,166):Color.rgb(55,85,98);TextView cell=label(dd+"\n"+exp,12);cell.setGravity(Gravity.CENTER);cell.setTextColor(Color.WHITE);cell.setBackground(refBg(Color.rgb(7,32,44),border,14));cell.setOnClickListener(v->dayPeople(day));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,58,1);lp.setMargins(2,2,2,2);line.addView(cell,lp);}body.addView(line);}
  LinearLayout leg=new LinearLayout(this);leg.setOrientation(LinearLayout.HORIZONTAL);String[] lt={"● Trabaja","● Franco","● Incidencia"};int[] lc={Color.rgb(48,205,166),Color.rgb(100,130,140),Color.rgb(235,82,82)};for(int i=0;i<3;i++){TextView v=label(lt[i],9);v.setTextColor(lc[i]);v.setGravity(Gravity.CENTER);leg.addView(v,new LinearLayout.LayoutParams(0,34,1));}body.addView(leg);exactBottom("TURNOS");
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Exact TURNOS screen now uses live monthly diagram.
s=s.replace('void exactTurns(){\n  currentScreen="CALENDARIO";base("TURNOS");body.addView(refHero("TURNOS","Seguridad"));touchCalendar();\n }','void exactTurns(){ exactDynamicTurns(); }')
s=s.replace('V31 LIVE DATA','V32 DYNAMIC TURNS')
p.write_text(s)
print("V32 dynamic turns applied")
