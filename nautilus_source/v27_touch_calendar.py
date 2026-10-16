from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 ImageView employeePhoto(String pid,int size){
  ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);im.setBackground(refBg(Color.rgb(20,55,68),Color.rgb(193,145,42),size));
  String[] a=personMaster(pid);try{if(a.length>11&&!a[11].isEmpty())im.setImageURI(android.net.Uri.parse(a[11]));}catch(Exception ignored){}
  im.setLayoutParams(new LinearLayout.LayoutParams(size,size));return im;
 }
 LinearLayout employeeDayCard(String pid,String name,String sec,String detail,String status,int accent){
  LinearLayout card=new LinearLayout(this);card.setOrientation(LinearLayout.HORIZONTAL);card.setGravity(Gravity.CENTER_VERTICAL);card.setPadding(12,12,12,12);card.setBackground(refBg(Color.rgb(12,34,45),Color.rgb(35,71,84),22));
  card.addView(employeePhoto(pid,64));LinearLayout mid=new LinearLayout(this);mid.setOrientation(LinearLayout.VERTICAL);mid.setPadding(14,0,8,0);TextView n=label(name,16);n.setTextColor(Color.WHITE);n.setTypeface(android.graphics.Typeface.DEFAULT,android.graphics.Typeface.BOLD);TextView d=label(sec+"\n"+detail,11);d.setTextColor(Color.rgb(160,190,200));mid.addView(n);mid.addView(d);card.addView(mid,new LinearLayout.LayoutParams(0,-2,1));card.addView(refChip(status,accent));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,-2);lp.setMargins(0,5,0,5);card.setLayoutParams(lp);return card;
 }
 void touchCalendar(){
  currentScreen="CALENDARIO";base("ALMANAQUE");Calendar cal=Calendar.getInstance();String month=new SimpleDateFormat("MMMM yyyy",new Locale("es","AR")).format(cal.getTime());body.addView(refHero(month.toUpperCase(new Locale("es","AR")),"Tocá un día para ver quién debía trabajar"));
  LinearLayout week=new LinearLayout(this);week.setOrientation(LinearLayout.HORIZONTAL);for(String x:new String[]{"L","M","X","J","V","S","D"}){TextView v=label(x,10);v.setGravity(Gravity.CENTER);v.setTextColor(Color.rgb(244,190,46));week.addView(v,new LinearLayout.LayoutParams(0,36,1));}body.addView(week);
  Calendar first=(Calendar)cal.clone();first.set(Calendar.DAY_OF_MONTH,1);int offset=(first.get(Calendar.DAY_OF_WEEK)+5)%7,max=cal.getActualMaximum(Calendar.DAY_OF_MONTH),day=1;
  for(int row=0;row<6&&day<=max;row++){LinearLayout line=new LinearLayout(this);line.setOrientation(LinearLayout.HORIZONTAL);for(int col=0;col<7;col++){if(row==0&&col<offset){line.addView(new TextView(this),new LinearLayout.LayoutParams(0,54,1));continue;}if(day>max){line.addView(new TextView(this),new LinearLayout.LayoutParams(0,54,1));continue;}final int dd=day++;String date=String.format(Locale.US,"%04d-%02d-%02d",cal.get(Calendar.YEAR),cal.get(Calendar.MONTH)+1,dd);int expected=0;Cursor c=db.getReadableDatabase().rawQuery("SELECT id FROM people WHERE active=1",null);while(c.moveToNext()){DayResult r=calcDay(c.getString(0),date);if(r!=null&&r.expected)expected++;}c.close();TextView cell=label(dd+"\n"+expected,12);cell.setGravity(Gravity.CENTER);cell.setTextColor(Color.WHITE);cell.setBackground(refBg(Color.rgb(13,38,49),dd==cal.get(Calendar.DAY_OF_MONTH)?Color.rgb(244,190,46):Color.rgb(35,71,84),14));cell.setOnClickListener(v->dayPeople(date));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,54,1);lp.setMargins(2,2,2,2);line.addView(cell,lp);}body.addView(line);}
  TextView foot=label("Número inferior: personal programado según diagrama",10);foot.setTextColor(Color.rgb(145,175,185));body.addView(foot);
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Day roster uses actual photo card and historical sector.
old='LinearLayout card=referenceRow("●",name,sec+" · "+punches,st,col);final String fp=pid;card.setOnClickListener(v->employeeDayProfile(fp,day));body.addView(card);'
new='sec=sectorForDate(pid,day);LinearLayout card=employeeDayCard(pid,name,sec,punches,st,col);final String fp=pid;card.setOnClickListener(v->employeeDayProfile(fp,day));body.addView(card);'
s=s.replace(old,new)
# Main dashboard calendar entry now opens tactile calendar.
s=s.replace('btn("ABRIR ALMANAQUE",this::calendarMonth);','btn("ABRIR ALMANAQUE",this::touchCalendar);')
# Bottom TURNOS route: if literal exists, point to calendar-first experience.
s=s.replace('navItem("TURNOS",this::calendarMonth','navItem("CALENDARIO",this::touchCalendar')
s=s.replace('V26 PERSONNEL MASTER','V27 TOUCH CALENDAR')
p.write_text(s)
print("V27 touch calendar + employee photos applied")
