from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 android.graphics.drawable.GradientDrawable refBg(int fill,int stroke,float radius){
  android.graphics.drawable.GradientDrawable g=new android.graphics.drawable.GradientDrawable();g.setColor(fill);g.setCornerRadius(radius);if(stroke!=0)g.setStroke(1,stroke);return g;
 }
 TextView refChip(String text,int color){
  TextView v=label(text,10);v.setTextColor(color);v.setGravity(Gravity.CENTER);v.setPadding(12,7,12,7);v.setBackground(refBg(Color.rgb(10,32,43),color,30));return v;
 }
 LinearLayout refHero(String title,String subtitle){
  LinearLayout h=new LinearLayout(this);h.setOrientation(LinearLayout.VERTICAL);h.setPadding(22,28,22,24);h.setBackground(refBg(Color.rgb(9,38,52),Color.rgb(193,145,42),28));
  TextView brand=label("NAUTILUS COUNTRY",11);brand.setTextColor(Color.rgb(244,190,46));brand.setLetterSpacing(.14f);h.addView(brand);
  TextView t=label(title,25);t.setTextColor(Color.WHITE);t.setTypeface(Typeface.DEFAULT,Typeface.BOLD);h.addView(t);
  TextView sub=label(subtitle,12);sub.setTextColor(Color.rgb(160,205,218));h.addView(sub);return h;
 }
 void employeeMetricStrip(String id){
  Calendar cc=Calendar.getInstance();String ym=new SimpleDateFormat("yyyy-MM",Locale.US).format(cc.getTime());int max=cc.getActualMaximum(Calendar.DAY_OF_MONTH),exp=0,pre=0,abs=0,late=0;
  for(int d=1;d<=max;d++){String day=String.format(Locale.US,"%s-%02d",ym,d);DayResult r=calcDay(id,day);if(r!=null&&r.expected){exp++;if(r.worked>0)pre++;else abs++;if(r.late>0)late++;}}
  LinearLayout row=new LinearLayout(this);row.setOrientation(LinearLayout.HORIZONTAL);String[] a={exp==0?"—":Math.round(pre*100f/exp)+"%",""+pre,""+abs,""+late};String[] b={"Presentismo","Trabajados","Ausencias","Tardanzas"};
  for(int i=0;i<4;i++){LinearLayout box=new LinearLayout(this);box.setOrientation(LinearLayout.VERTICAL);box.setGravity(Gravity.CENTER);box.setPadding(4,12,4,12);box.setBackground(refBg(Color.rgb(13,38,49),Color.rgb(35,71,84),18));TextView n=label(a[i],18);n.setTextColor(i==2&&abs>0?Color.rgb(235,82,82):Color.rgb(48,205,166));n.setTypeface(Typeface.DEFAULT,Typeface.BOLD);n.setGravity(Gravity.CENTER);TextView q=label(b[i],9);q.setTextColor(Color.rgb(160,185,195));q.setGravity(Gravity.CENTER);box.addView(n);box.addView(q);LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,-2,1);lp.setMargins(3,0,3,0);row.addView(box,lp);}body.addView(row);
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Strengthen dashboard top hero.
needle='operationBanner(totalExpected,totalPresent,totalAbsent,totalLate);'
if needle in s:s=s.replace(needle,'body.addView(refHero("PRESENTISMO","Control operativo · "+new SimpleDateFormat("EEEE d \'de\' MMMM",new Locale("es","AR")).format(new Date())));'+needle,1)
# Employee profile: insert visual hero + metrics after active status when id is in scope.
needle2='body.addView(statusPill("● ACTIVO",Color.rgb(48,205,166)));'
if needle2 in s:s=s.replace(needle2,'body.addView(refHero(name,sector+" · "+regime));'+needle2+'employeeMetricStrip(id);',1)
# Reports / More visual cover.
s=s.replace('void reports(){currentScreen="INFORMES";base("INFORMES");','void reports(){currentScreen="INFORMES";base("INFORMES");body.addView(refHero("INFORMES","Presentismo · incidencias · horas"));')
s=s.replace('void moreMenu(){currentScreen="MÁS";base("MÁS");','void moreMenu(){currentScreen="MÁS";base("MÁS");body.addView(refHero("MÁS OPCIONES","Administración del sistema"));')
s=s.replace('V21 VISUAL MASTER','V22 VISUAL REACTOR')
p.write_text(s)
print("V22 visual reactor applied")
