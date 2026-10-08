from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# V16: active bottom navigation and tighter reference proportions.
s=s.replace('void bottomNav(LinearLayout root){LinearLayout n=new LinearLayout(this);', 'void bottomNav(LinearLayout root){LinearLayout n=new LinearLayout(this);')
old='void nav(LinearLayout n,String text,Runnable r){Button b=new Button(this);b.setText(text);b.setAllCaps(false);b.setTextSize(10);b.setTextColor(Color.rgb(225,238,242));b.setGravity(Gravity.CENTER);b.setBackgroundColor(Color.TRANSPARENT);b.setOnClickListener(v->r.run());n.addView(b,new LinearLayout.LayoutParams(0,-2,1));}'
new='''void nav(LinearLayout n,String text,Runnable r){Button b=new Button(this);b.setText(text);b.setAllCaps(false);b.setTextSize(10);boolean active=(currentScreen!=null&&text.contains(currentScreen));b.setTextColor(active?Color.rgb(244,190,46):Color.rgb(180,205,214));b.setGravity(Gravity.CENTER);android.graphics.drawable.GradientDrawable g=new android.graphics.drawable.GradientDrawable();g.setColor(active?Color.rgb(16,42,53):Color.TRANSPARENT);g.setCornerRadius(18);if(active)g.setStroke(1,Color.rgb(244,190,46));b.setBackground(g);b.setOnClickListener(v->r.run());LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,-2,1);lp.setMargins(2,0,2,0);n.addView(b,lp);}'''
if old in s:s=s.replace(old,new)
# Set active screen names at primary destinations.
for a,b in [
 ('void todayDashboard(){base("HOY");','void todayDashboard(){currentScreen="HOY";base("HOY");'),
 ('void employeeDirectory(){base("PERSONAL");','void employeeDirectory(){currentScreen="PERSONAL";base("PERSONAL");'),
 ('void calendarMonth(){base("TURNOS");','void calendarMonth(){currentScreen="TURNOS";base("TURNOS");'),
 ('void reports(){base("INFORMES");','void reports(){currentScreen="INFORMES";base("INFORMES");'),
 ('void moreMenu(){base("MÁS");','void moreMenu(){currentScreen="MÁS";base("MÁS");')
]: s=s.replace(a,b)
# A compact month grid visual component using actual current month day count.
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 void referenceMonthGrid(){
  Calendar cal=Calendar.getInstance();int max=cal.getActualMaximum(Calendar.DAY_OF_MONTH);int first=cal.get(Calendar.DAY_OF_MONTH);cal.set(Calendar.DAY_OF_MONTH,1);int offset=(cal.get(Calendar.DAY_OF_WEEK)+5)%7;cal.set(Calendar.DAY_OF_MONTH,first);
  LinearLayout days=new LinearLayout(this);days.setOrientation(LinearLayout.HORIZONTAL);for(String d:new String[]{"L","M","X","J","V","S","D"}){TextView x=label(d,10);x.setTextColor(Color.rgb(140,175,188));x.setGravity(Gravity.CENTER);days.addView(x,new LinearLayout.LayoutParams(0,-2,1));}body.addView(days);
  int n=1;for(int row=0;row<6&&n<=max;row++){LinearLayout line=new LinearLayout(this);line.setOrientation(LinearLayout.HORIZONTAL);for(int col=0;col<7;col++){TextView cell=label("",12);cell.setGravity(Gravity.CENTER);cell.setPadding(2,12,2,12);if(row*7+col>=offset&&n<=max){cell.setText(""+n);int dow=col;int accent=(dow>=5)?Color.rgb(80,145,190):Color.rgb(48,205,166);android.graphics.drawable.GradientDrawable g=new android.graphics.drawable.GradientDrawable();g.setColor(Color.rgb(10,33,44));g.setCornerRadius(12);g.setStroke(1,accent);cell.setBackground(g);cell.setTextColor(Color.WHITE);n++;}LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,-2,1);lp.setMargins(2,2,2,2);line.addView(cell,lp);}body.addView(line);}}
'''
s=s.replace(mark,code+"\n"+mark)
# Place grid in Turnos.
needle='body.addView(premiumCard("TURNOS","CALENDARIO MENSUAL","Trabajo · franco · licencia · incidencia",Color.rgb(66,185,220)));'
if needle in s:s=s.replace(needle,needle+'referenceMonthGrid();',1)
# Reference sector title and employee tabs.
s=s.replace('base(sector);sectionTitle("COBERTURA","Personal esperado y estado actual");','base(sector);body.addView(statusPill("COBERTURA DEL SECTOR",Color.rgb(48,205,166)));sectionTitle("HOY     TURNOS     CALENDARIO","Personal esperado y estado actual");')
# Make employee header closer to reference with active status.
needle2='String name=c.getString(0),sector=c.getString(1),regime=c.getString(2);c.close();'
if needle2 in s:s=s.replace(needle2,needle2+'body.addView(statusPill("● ACTIVO",Color.rgb(48,205,166)));')
# Version marker
s=s.replace('V15 REFERENCE','V16 NUCLEAR')
p.write_text(s)
print("V16 nuclear visual fidelity applied")
