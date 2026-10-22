from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void dualClockHub(){'
assert mark in s
code=r'''
 void chooseSummaryMonth(int year){
  currentScreen="MESES";mtScreen("RESUMEN DEL MES · ELEGIR MES",3);
  body.addView(mtText("Seleccioná el año y después el mes que querés consultar. Incluye las fichadas del reloj importadas.",13,mtPale(),false));
  LinearLayout selector=new LinearLayout(this);selector.setOrientation(LinearLayout.HORIZONTAL);
  TextView prev=mtText("‹  AÑO",15,mtGold(),true);prev.setGravity(Gravity.CENTER);
  prev.setOnClickListener(v->chooseSummaryMonth(year-1));
  TextView current=mtText(String.valueOf(year),24,Color.WHITE,true);current.setGravity(Gravity.CENTER);
  TextView next=mtText("AÑO  ›",15,mtGold(),true);next.setGravity(Gravity.CENTER);
  next.setOnClickListener(v->chooseSummaryMonth(year+1));
  selector.addView(prev,new LinearLayout.LayoutParams(0,mtDp(64),1));
  selector.addView(current,new LinearLayout.LayoutParams(0,mtDp(64),1));
  selector.addView(next,new LinearLayout.LayoutParams(0,mtDp(64),1));
  body.addView(selector);
  String[] months={"ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"};
  for(int i=0;i<12;i++){
   final int m=i;
   Calendar c=Calendar.getInstance();c.clear();c.set(year,m,1,12,0,0);
   final Date target=c.getTime(),monthDate=target;
   String from=rpDate(target),to=rpMonthEnd(target);
   Cursor count=db.getReadableDatabase().rawQuery("SELECT COUNT(*),COUNT(DISTINCT person_id) FROM punches WHERE substr(stamp,1,10) BETWEEN ? AND ?",new String[]{from,to});
   int records=0,people=0;
   try{if(count.moveToFirst()){records=count.getInt(0);people=count.getInt(1);}}finally{count.close();}
   mtAddLink("▦",months[i]+" "+year,records+" fichadas · "+people+" empleados",()->rpPeriod(monthDate,true));
  }
  mtAddLink("◷","VOLVER AL MES ACTUAL","Abrir el informe de este mes",()->rpPeriod(new Date(),true));
 }
 void chooseSummaryMonth(){
  Calendar now=Calendar.getInstance();
  chooseSummaryMonth(now.get(Calendar.YEAR));
 }
'''
s=s.replace(mark,code+'\n'+mark,1)
old='mtPanelTitle("RESUMEN DEL MES","VER MESES  ›",()->rpPeriod(new Date(),true))'
if old in s:s=s.replace(old,'mtPanelTitle("RESUMEN DEL MES","VER MESES  ›",this::chooseSummaryMonth)')
else:
 print("No exact panel match; searching fallback")
 s=s.replace('mtPanelTitle("RESUMEN DEL MES","VER DETALLE  ›",()->quickReport(true))','mtPanelTitle("RESUMEN DEL MES","VER MESES  ›",this::chooseSummaryMonth)')
# Also expose selector from reports, without losing period navigation.
s=s.replace('mtAddLink("▥","INFORME MENSUAL","Elegí meses anteriores o posteriores",()->rpPeriod(new Date(),true));',
'''mtAddLink("▥","INFORME MENSUAL","Elegí el año y el mes",this::chooseSummaryMonth);''',1)
assert 'void chooseSummaryMonth(int year)' in s
p.write_text(s)
print("V75: year selector + twelve months with grounded real punch counts; summary month picker linked")
