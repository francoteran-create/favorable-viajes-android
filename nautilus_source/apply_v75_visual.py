from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()

old='void base(String title){ScrollView sv=new ScrollView(this);body=new LinearLayout(this);body.setOrientation(LinearLayout.VERTICAL);body.setPadding(20,26,20,28);body.setBackgroundColor(BG);sv.addView(body);TextView h=label(title,25);h.setTextColor(CYAN);body.addView(h);setContentView(sv);}'
new='''void base(String title){
 LinearLayout root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setBackgroundColor(BG);
 ScrollView sv=new ScrollView(this);body=new LinearLayout(this);body.setOrientation(LinearLayout.VERTICAL);body.setPadding(20,22,20,24);body.setBackgroundColor(BG);sv.addView(body);
 TextView brand=label("〰  NAUTILUS COUNTRY",20);brand.setTextColor(Color.rgb(244,190,46));brand.setGravity(Gravity.CENTER);body.addView(brand);
 TextView sub=label("P R E S E N T I S M O",11);sub.setTextColor(Color.WHITE);sub.setGravity(Gravity.CENTER);body.addView(sub);
 TextView h=label(title,24);h.setTextColor(Color.WHITE);body.addView(h);
 root.addView(sv,new LinearLayout.LayoutParams(-1,0,1));
 bottomNav(root);setContentView(root);
}'''
assert old in s
s=s.replace(old,new)

old='void btn(String s,Runnable r){Button b=new Button(this);b.setText(s);b.setAllCaps(false);b.setTextSize(16);b.setOnClickListener(v->r.run());body.addView(b,new LinearLayout.LayoutParams(-1,-2));}'
new='''void btn(String s,Runnable r){Button b=new Button(this);b.setText(s);b.setAllCaps(false);b.setTextSize(15);b.setTextColor(Color.WHITE);b.setPadding(14,14,14,14);android.graphics.drawable.GradientDrawable g=new android.graphics.drawable.GradientDrawable();g.setColor(Color.rgb(10,31,42));g.setCornerRadius(18);g.setStroke(1,Color.rgb(33,104,132));b.setBackground(g);b.setOnClickListener(v->r.run());LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,-2);lp.setMargins(0,5,0,5);body.addView(b,lp);}'''
assert old in s
s=s.replace(old,new)

home=re.search(r' void home\(\)\{.*?\}\n String stats\(\)',s,re.S)
assert home
replacement=''' void home(){todayDashboard();}
 void bottomNav(LinearLayout root){LinearLayout n=new LinearLayout(this);n.setOrientation(LinearLayout.HORIZONTAL);n.setPadding(5,7,5,7);n.setBackgroundColor(Color.rgb(5,20,29));nav(n,"⌂\\nHOY",this::todayDashboard);nav(n,"♙\\nPERSONAL",this::employees);nav(n,"▣\\nTURNOS",this::calendarMonth);nav(n,"▤\\nINFORMES",this::reports);nav(n,"☰\\nMÁS",this::moreMenu);root.addView(n,new LinearLayout.LayoutParams(-1,-2));}
 void nav(LinearLayout n,String text,Runnable r){Button b=new Button(this);b.setText(text);b.setAllCaps(false);b.setTextSize(10);b.setTextColor(Color.rgb(205,231,240));b.setGravity(Gravity.CENTER);b.setBackgroundColor(Color.TRANSPARENT);b.setOnClickListener(v->r.run());n.addView(b,new LinearLayout.LayoutParams(0,-2,1));}
 void moreMenu(){base("MÁS OPCIONES");body.addView(muted("Administración y configuración del sistema"));btn("IMPORTAR FICHADAS · Attendance logs.xls",this::pick);btn("EMPLEADOS",this::employees);btn("SECTORES Y REGÍMENES",this::regimes);btn("SIMULADOR DE TURNOS",this::shiftSimulator);btn("COBERTURA MÍNIMA",this::coverageSetup);btn("CALENDARIO / EXCEPCIONES",this::overrides);btn("REVISAR INCIDENCIAS",this::reviews);btn("DIAGNÓSTICO DE JORNADA",this::diagnosticPicker);btn("CIERRE MENSUAL",this::monthClose);btn("RESUMEN PARA LIQUIDACIÓN",this::payrollSummary);btn("PENDIENTES DE CONFIGURAR",this::pending);btn("MARCACIONES DEL RELOJ",this::logs);}
 String stats()'''
s=s[:home.start()]+replacement+s[home.end():]

# Dashboard: no redundant back button on primary tab, stronger operational header.
s=s.replace('void todayDashboard(){base("NAUTILUS · HOY");back();','void todayDashboard(){base("HOY");')
s=s.replace('body.addView(label(String.format(Locale.US,"PRESENTISMO HOY %.1f%%\\nEsperados %d · Presentes %d · Ausentes %d · Tardanzas %d · Incidencias %d",pct,totalExpected,totalPresent,totalAbsent,totalLate,totalInc),18));',
'''TextView hero=label((totalAbsent==0?"✓  OPERACIÓN NORMAL":"⚠  REQUIERE ATENCIÓN")+"\\n"+String.format(Locale.US,"Presentismo %.1f%%  ·  Esperados %d  ·  Presentes %d  ·  Ausentes %d  ·  Tarde %d",pct,totalExpected,totalPresent,totalAbsent,totalLate),18);android.graphics.drawable.GradientDrawable hg=new android.graphics.drawable.GradientDrawable();hg.setColor(totalAbsent==0?Color.rgb(4,65,45):Color.rgb(76,38,18));hg.setCornerRadius(22);hg.setStroke(2,totalAbsent==0?Color.rgb(31,220,130):Color.rgb(244,190,46));hero.setBackground(hg);body.addView(hero);''')

# Primary tabs shouldn't show a big back-to-home button.
s=s.replace('void reports(){base("INFORMES");back();','void reports(){base("INFORMES");')
s=s.replace('void calendarMonth(){base("CALENDARIO MENSUAL");back();','void calendarMonth(){base("TURNOS · CALENDARIO");')
s=s.replace('void employees(){base("EMPLEADOS");back();','void employees(){base("PERSONAL");')

p.write_text(s)
print("visual shell applied",len(s))
