from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=" void mtWeek(Date focus){"
assert mark in s
code=r'''
 void mtCalendar(Date focus){
  currentScreen="CALENDARIO";mtScreen("TURNOS · CALENDARIO MENSUAL",1);
  Calendar cal=Calendar.getInstance();cal.setTime(focus);cal.set(Calendar.DAY_OF_MONTH,1);
  final int year=cal.get(Calendar.YEAR),month=cal.get(Calendar.MONTH);
  LinearLayout bar=new LinearLayout(this);bar.setOrientation(LinearLayout.HORIZONTAL);bar.setGravity(Gravity.CENTER_VERTICAL);
  TextView prev=mtText("‹",29,mtGold(),true);prev.setGravity(Gravity.CENTER);prev.setContentDescription("Mes anterior");
  prev.setOnClickListener(v->{Calendar x=(Calendar)cal.clone();x.add(Calendar.MONTH,-1);mtCalendar(x.getTime());});
  TextView heading=mtText(new SimpleDateFormat("MMMM yyyy",new Locale("es","AR")).format(cal.getTime()).toUpperCase(new Locale("es","AR")),17,Color.WHITE,true);heading.setGravity(Gravity.CENTER);
  TextView next=mtText("›",29,mtGold(),true);next.setGravity(Gravity.CENTER);next.setContentDescription("Mes siguiente");
  next.setOnClickListener(v->{Calendar x=(Calendar)cal.clone();x.add(Calendar.MONTH,1);mtCalendar(x.getTime());});
  bar.addView(prev,new LinearLayout.LayoutParams(mtDp(54),mtDp(56)));
  bar.addView(heading,new LinearLayout.LayoutParams(0,mtDp(56),1));
  bar.addView(next,new LinearLayout.LayoutParams(mtDp(54),mtDp(56)));body.addView(bar);
  LinearLayout days=new LinearLayout(this);days.setOrientation(LinearLayout.HORIZONTAL);
  for(String label:new String[]{"LUN","MAR","MIÉ","JUE","VIE","SÁB","DOM"}){
   TextView d=mtText(label,10,mtGold(),true);d.setGravity(Gravity.CENTER);
   days.addView(d,new LinearLayout.LayoutParams(0,mtDp(34),1));
  }body.addView(days);
  int first=(cal.get(Calendar.DAY_OF_WEEK)+5)%7;
  int max=cal.getActualMaximum(Calendar.DAY_OF_MONTH);
  for(int week=0;week<6;week++){
   if(week*7-first>=max)break;
   LinearLayout line=new LinearLayout(this);line.setOrientation(LinearLayout.HORIZONTAL);
   for(int col=0;col<7;col++){
    int day=week*7+col-first+1;
    LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,mtDp(76),1);
    lp.setMargins(mtDp(2),mtDp(3),mtDp(2),mtDp(3));
    if(day<1||day>max){line.addView(new TextView(this),lp);continue;}
    final String date=String.format(Locale.US,"%04d-%02d-%02d",year,month+1,day);
    LinearLayout cell=new LinearLayout(this);cell.setOrientation(LinearLayout.VERTICAL);cell.setGravity(Gravity.CENTER);
    Calendar today=Calendar.getInstance();
    boolean selected=year==today.get(Calendar.YEAR)&&month==today.get(Calendar.MONTH)&&day==today.get(Calendar.DAY_OF_MONTH);
    cell.setBackground(mtBg(selected?0xFF114766:0xFF0A2B40,0xFF031524,selected?0xFF34C4FF:0xFF345E76,12));
    TextView number=mtText(""+day,19,Color.WHITE,true);number.setGravity(Gravity.CENTER);
    TextView lower=mtText("VER",9,selected?mtGold():mtPale(),true);lower.setGravity(Gravity.CENTER);
    cell.addView(number,new LinearLayout.LayoutParams(-1,mtDp(36)));
    cell.addView(lower,new LinearLayout.LayoutParams(-1,mtDp(23)));
    cell.setContentDescription(date+" · ver personal diagramado");
    cell.setOnClickListener(v->mtDayRoster(date));line.addView(cell,lp);
   }
   body.addView(line,new LinearLayout.LayoutParams(-1,mtDp(82)));
  }
  mtAddLink("▣","VOLVER A SEMANA","Ver planificación de lunes a domingo",()->mtWeek(focus));
 }
'''
s=s.replace(mark,code+"\n"+mark,1)
# Prominent entry at the top of modern weekly planning.
needle='void mtWeek(Date focus){\n  currentScreen="SEMANA";mtScreen("TURNOS · SEMANA",1);'
assert needle in s
s=s.replace(needle,needle+'\n  mtAddLink("▦","VER CALENDARIO MENSUAL","Días grandes · avanzar y retroceder meses",()->mtCalendar(focus));',1)
# Historic shortcut should also open the same usable monthly calendar.
s=s.replace('btn("ABRIR ALMANAQUE",this::touchCalendar);','btn("ABRIR ALMANAQUE",()->mtCalendar(new Date()));')
p.write_text(s)
print("V64 monthly calendar with 76dp cells, month navigation, weekly access")
