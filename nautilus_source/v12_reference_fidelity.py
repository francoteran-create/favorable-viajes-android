from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 TextView goldRule(){TextView v=new TextView(this);v.setBackgroundColor(Color.rgb(220,164,36));v.setHeight(2);return v;}
 LinearLayout referenceHeader(String title,String subtitle){
  LinearLayout box=new LinearLayout(this);box.setOrientation(LinearLayout.VERTICAL);box.setPadding(14,8,14,10);
  TextView wave=label("〰",27);wave.setTextColor(Color.rgb(244,190,46));wave.setGravity(Gravity.CENTER);box.addView(wave);
  TextView brand=label("NAUTILUS COUNTRY",18);brand.setTextColor(Color.WHITE);brand.setGravity(Gravity.CENTER);brand.setLetterSpacing(.08f);box.addView(brand);
  TextView pr=label("P R E S E N T I S M O",9);pr.setTextColor(Color.WHITE);pr.setGravity(Gravity.CENTER);pr.setLetterSpacing(.20f);box.addView(pr);
  if(title!=null&&!title.isEmpty()){TextView t=label(title,25);t.setTextColor(Color.WHITE);t.setPadding(0,10,0,0);box.addView(t);}
  if(subtitle!=null&&!subtitle.isEmpty()){TextView d=label(subtitle,12);d.setTextColor(Color.rgb(150,185,198));box.addView(d);}
  return box;
 }
 LinearLayout referenceRow(String icon,String title,String detail,String right,int accent){
  LinearLayout row=new LinearLayout(this);row.setOrientation(LinearLayout.HORIZONTAL);row.setGravity(Gravity.CENTER_VERTICAL);row.setPadding(14,12,14,12);
  android.graphics.drawable.GradientDrawable g=new android.graphics.drawable.GradientDrawable();g.setColor(Color.rgb(8,31,43));g.setCornerRadius(18);g.setStroke(1,Color.rgb(28,71,91));row.setBackground(g);
  TextView ic=label(icon,20);ic.setTextColor(accent);ic.setGravity(Gravity.CENTER);row.addView(ic,new LinearLayout.LayoutParams(42,-2));
  LinearLayout mid=new LinearLayout(this);mid.setOrientation(LinearLayout.VERTICAL);TextView a=label(title,15);a.setTextColor(Color.WHITE);mid.addView(a);TextView b=label(detail,11);b.setTextColor(Color.rgb(158,188,198));mid.addView(b);row.addView(mid,new LinearLayout.LayoutParams(0,-2,1));
  TextView rr=label(right,14);rr.setTextColor(accent);rr.setGravity(Gravity.RIGHT|Gravity.CENTER_VERTICAL);row.addView(rr,new LinearLayout.LayoutParams(-2,-2));
  return row;
 }
 void addRefRow(String icon,String title,String detail,String right,int accent,Runnable action){LinearLayout r=referenceRow(icon,title,detail,right,accent);if(action!=null)r.setOnClickListener(v->action.run());LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,-2);lp.setMargins(0,4,0,4);body.addView(r,lp);}
'''
s=s.replace(mark,code+"\n"+mark)
# Exact-reference style base: remove duplicate generic page title hierarchy and use compact brand.
old='TextView brand=label("◉  NAUTILUS COUNTRY",21);brand.setTextColor(Color.rgb(244,190,46));brand.setGravity(Gravity.CENTER);body.addView(brand);\n TextView sub=label("P R E S E N T I S M O   ·   V10 VISUAL",10);sub.setTextColor(Color.WHITE);sub.setGravity(Gravity.CENTER);body.addView(sub);\n TextView h=label(title,24);h.setTextColor(Color.WHITE);body.addView(h);'
new='body.addView(referenceHeader(title,""));'
if old in s:s=s.replace(old,new)
# More screen mapped to reference architecture
start='void moreMenu(){base("MÁS");sectionTitle("ADMINISTRACIÓN","Configuración, importación y herramientas del sistema");body.addView(statusPill("NAUTILUS PRESENTISMO · V11 DESIGN",Color.rgb(244,190,46)));'
if start in s:
 s=s.replace(start,start+'addRefRow("♙","Empleados","Gestionar personal","›",Color.rgb(244,190,46),this::employeeDirectory);addRefRow("⚙","Sectores","Configurar sectores","›",Color.rgb(244,190,46),this::regimes);addRefRow("▣","Regímenes de turno","4x2, 2x2, 5x2, etc.","›",Color.rgb(244,190,46),this::regimes);addRefRow("♜","Cobertura mínima","Definir requerimientos por sector","›",Color.rgb(244,190,46),this::coverageSetup);')
# Reports reference rows at top
needle='void reports(){base("INFORMES");sectionTitle("CENTRO DE INFORMES","Presentismo, incidencias, horas y liquidación");body.addView(premiumCard("INFORME MENSUAL","RESUMEN EJECUTIVO","Presentismo · horas · novedades",Color.rgb(244,190,46)));'
if needle in s:
 s=s.replace(needle,needle+'addRefRow("▤","Informe mensual","Presentismo por empleado y sector","›",Color.rgb(244,190,46),this::monthClose);addRefRow("⚠","Informe de incidencias","Tardanzas, ausencias, marcaciones","›",Color.rgb(244,190,46),this::reviews);addRefRow("◷","Informe de horas","Trabajadas, extras, por sector","›",Color.rgb(244,190,46),this::payrollSummary);')
p.write_text(s)
print("V12 reference fidelity shell applied")
