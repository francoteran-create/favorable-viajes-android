from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# Premium visual primitives
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 TextView kicker(String t){TextView v=label(t.toUpperCase(Locale.US),11);v.setTextColor(Color.rgb(244,190,46));v.setLetterSpacing(.16f);v.setPadding(2,12,2,5);return v;}
 TextView premiumCard(String title,String value,String detail,int accent){TextView v=label(title.toUpperCase(Locale.US)+"\n"+value+"\n"+detail,16);v.setTextColor(Color.WHITE);v.setPadding(20,18,20,18);android.graphics.drawable.GradientDrawable g=new android.graphics.drawable.GradientDrawable();g.setOrientation(android.graphics.drawable.GradientDrawable.Orientation.TL_BR);g.setColors(new int[]{Color.rgb(15,43,57),Color.rgb(7,24,34)});g.setCornerRadius(28);g.setStroke(2,accent);v.setBackground(g);LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,-2);lp.setMargins(0,7,0,7);v.setLayoutParams(lp);return v;}
 void sectionTitle(String t,String d){body.addView(kicker(t));TextView x=label(d,13);x.setTextColor(Color.rgb(150,180,190));x.setPadding(2,0,2,8);body.addView(x);}
'''
s=s.replace(mark,code+"\n"+mark)
# Stronger brand and spacing
s=s.replace('TextView brand=label("〰  NAUTILUS COUNTRY",20);','TextView brand=label("◉  NAUTILUS COUNTRY",21);')
s=s.replace('TextView sub=label("P R E S E N T I S M O",11);','TextView sub=label("P R E S E N T I S M O   ·   V10 VISUAL",10);')
# Bottom nav more premium
s=s.replace('n.setPadding(5,7,5,7);n.setBackgroundColor(Color.rgb(5,20,29));','n.setPadding(4,10,4,10);n.setBackgroundColor(Color.rgb(3,15,23));')
s=s.replace('b.setTextSize(10);b.setTextColor(Color.rgb(205,231,240));','b.setTextSize(10);b.setTextColor(Color.rgb(225,238,242));')
# Dashboard opening hero/date
needle='void todayDashboard(){base("HOY");'
s=s.replace(needle,needle+'body.addView(kicker(new SimpleDateFormat("EEEE d · MMMM",new Locale("es","AR")).format(new Date())));TextView cover=premiumCard("NAUTILUS COUNTRY","CONTROL OPERATIVO","Asistencia · cobertura · novedades",Color.rgb(244,190,46));cover.setTextSize(19);cover.setGravity(Gravity.CENTER);cover.setPadding(22,28,22,28);body.addView(cover);')
# Employee directory visual header
s=s.replace('void employeeDirectory(){base("PERSONAL");','void employeeDirectory(){base("PERSONAL");sectionTitle("EQUIPO","Estado, régimen y desempeño de cada trabajador");')
# Reports visual header
s=s.replace('void reports(){base("INFORMES");','void reports(){base("INFORMES");sectionTitle("CENTRO DE INFORMES","Presentismo, incidencias, horas y liquidación");')
# More visual header
s=s.replace('void moreMenu(){base("MÁS OPCIONES");body.addView(muted("Administración y configuración del sistema"));','void moreMenu(){base("MÁS");sectionTitle("ADMINISTRACIÓN","Configuración, importación y herramientas del sistema");')
p.write_text(s)
print("V10 premium visual system applied")
