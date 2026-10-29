from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
def swap(name,code):
 global s
 m=re.search(r'\bvoid\s+'+re.escape(name)+r'\s*\([^)]*\)\s*\{',s);assert m,name
 st=s.index('{',m.start());d=0;q=None;esc=False
 for i in range(st,len(s)):
  x=s[i]
  if q:
   if esc:esc=False
   elif x=='\\':esc=True
   elif x==q:q=None
   continue
  if x in ('"',"'"):q=x;continue
  if x=='{':d+=1
  if x=='}':
   d-=1
   if d==0:s=s[:m.start()]+code+s[i+1:];return
 raise Exception(name)
extra=r'''
 // totals: attendance counts person/days, punches raw count, paired times only if safe.
 long[] h79WorkerTotals(String pid,String from,String to){
  long[] t=new long[7]; // days, punches, registered min, ordinary min, proposed extra min, review days, scheduled days
  rsEnsure();
  Cursor days=db.getReadableDatabase().rawQuery(
   "SELECT substr(stamp,1,10),COUNT(*) FROM punches WHERE person_id=? AND substr(stamp,1,10) BETWEEN ? AND ? GROUP BY substr(stamp,1,10) ORDER BY 1",
   new String[]{pid,from,to});
  try{while(days.moveToNext()){
   String day=days.getString(0);t[0]++;t[1]+=days.getInt(1);
   String[] v=hrDay(pid,day);
   if(v[1].equals("—"))t[5]++;
   else{
    int full=rsMinutes(v[1]),common=rsMinutes(v[2]),extra=rsMinutes(v[3]);
    if(full>=0)t[2]+=full;
    if(common>=0)t[3]+=common;
    if(extra>=0)t[4]+=extra;
   }
  }}finally{days.close();}
  Cursor shifts=db.getReadableDatabase().rawQuery(
   "SELECT COUNT(*) FROM scheduled_shifts WHERE person_id=? AND work_date BETWEEN ? AND ? AND start_time!='FRANCO'",
   new String[]{pid,from,to});
  try{if(shifts.moveToFirst())t[6]=shifts.getLong(0);}finally{shifts.close();}
  return t;
 }
 long[] h79AllTotals(String from,String to,String pid){
  long[] total=new long[8]; // 7 metrics + employees with days
  Cursor c=db.getReadableDatabase().rawQuery(
   "SELECT id FROM people WHERE active=1 "+(pid==null?"":"AND id=?")+" ORDER BY name",
   pid==null?null:new String[]{pid});
  try{while(c.moveToNext()){
   long[] n=h79WorkerTotals(c.getString(0),from,to);
   if(n[0]>0)total[7]++;
   for(int k=0;k<7;k++)total[k]+=n[k];
  }}finally{c.close();}
  return total;
 }
 void h79TotalsPanel(String from,String to){
  long[] n=h79AllTotals(from,to,null);
  LinearLayout panel=mtPanel();
  panel.addView(mtText("TOTAL GENERAL DEL PLANTEL",17,mtGold(),true));
  panel.addView(mtText(from+"  AL  "+to,11,mtPale(),false));
  String[] labels={"EMPLEADOS CON ASISTENCIA","DÍAS DE ASISTENCIA","FICHADAS REGISTRADAS","HORAS ENTRE MARCAS VÁLIDAS","HORAS COMUNES ESTIMADAS","HORAS DE RECARGO PROPUESTAS","DÍAS A REVISAR","TURNOS PROGRAMADOS"};
  String[] values={""+n[7],""+n[0],""+n[1],hrTime((int)n[2]),hrTime((int)n[3]),hrTime((int)n[4]),""+n[5],""+n[6]};
  for(int i=0;i<labels.length;i++){
   LinearLayout line=new LinearLayout(this);line.setOrientation(LinearLayout.HORIZONTAL);line.setPadding(mtDp(5),mtDp(6),mtDp(5),mtDp(6));
   TextView key=mtText(labels[i],11,mtPale(),false);
   TextView val=mtText(values[i],16,i==5?mtGold():Color.WHITE,true);val.setGravity(Gravity.RIGHT|Gravity.CENTER_VERTICAL);
   line.addView(key,new LinearLayout.LayoutParams(0,mtDp(34),3));
   line.addView(val,new LinearLayout.LayoutParams(0,mtDp(34),2));panel.addView(line);
  }
  panel.addView(mtText("HORAS INDICATIVAS: sólo pares válidos del mismo día. Los días con marcas incompletas o turnos nocturnos quedan pendientes de revisión y fuera de las horas calculadas. No son horas liquidadas.",11,mtPale(),false));
  body.addView(panel);
 }
 void h79MiniBars(String label,int[] vals,String[] months,int accent){
  body.addView(mtText(label,14,mtGold(),true));
  int max=1;for(int value:vals)max=Math.max(max,value);
  for(int j=0;j<vals.length;j++){
   LinearLayout line=new LinearLayout(this);line.setOrientation(LinearLayout.HORIZONTAL);line.setGravity(Gravity.CENTER_VERTICAL);
   TextView name=mtText(months[j],10,mtPale(),true);
   name.setGravity(Gravity.CENTER_VERTICAL);line.addView(name,new LinearLayout.LayoutParams(mtDp(67),mtDp(34)));
   LinearLayout outer=new LinearLayout(this);outer.setGravity(Gravity.LEFT|Gravity.CENTER_VERTICAL);
   outer.setBackground(mtBg(0xFF09253B,0xFF061A2C,0xFF1D4E69,7));
   android.view.View fill=new android.view.View(this);fill.setBackground(mtBg(accent,accent,accent,6));
   float ratio=(float)vals[j]/(float)max;int width=vals[j]==0?0:Math.max(mtDp(3),(int)(mtDp(155)*ratio));
   outer.addView(fill,new LinearLayout.LayoutParams(width,mtDp(17)));
   line.addView(outer,new LinearLayout.LayoutParams(0,mtDp(28),1));
   TextView v=mtText(""+vals[j],12,Color.WHITE,true);v.setGravity(Gravity.RIGHT|Gravity.CENTER_VERTICAL);
   line.addView(v,new LinearLayout.LayoutParams(mtDp(46),mtDp(34)));
   body.addView(line);
  }
 }
 void h79EmployeeCharts(String pid,String from){
  int year=Integer.parseInt(from.substring(0,4)),month=Integer.parseInt(from.substring(5,7));
  String[] labels=new String[6];int[] days=new int[6],marks=new int[6],common=new int[6],extra=new int[6];
  for(int k=0;k<6;k++){
   Calendar cal=Calendar.getInstance();cal.clear();cal.set(year,month-1,1);
   cal.add(Calendar.MONTH,k-5);
   String start=rpDate(cal.getTime()),end=rpMonthEnd(cal.getTime());
   labels[k]=new SimpleDateFormat("MM/yy",Locale.US).format(cal.getTime());
   long[] n=h79WorkerTotals(pid,start,end);
   days[k]=(int)n[0];marks[k]=(int)n[1];
   common[k]=(int)(n[3]/60);extra[k]=(int)(n[4]/60);
  }
  body.addView(mtText("EVOLUCIÓN DEL EMPLEADO · ÚLTIMOS 6 MESES HASTA EL ELEGIDO",13,Color.WHITE,true));
  body.addView(mtText("Cada fila representa un mes. Las horas de las barras están redondeadas hacia abajo; los totales exactos se conservan en HH:MM.",11,mtPale(),false));
  h79MiniBars("DÍAS CON ASISTENCIA",days,labels,0xFF39D88F);
  h79MiniBars("FICHADAS REGISTRADAS",marks,labels,0xFF66B7E9);
  h79MiniBars("HORAS COMUNES ESTIMADAS (h)",common,labels,0xFFF2C363);
  h79MiniBars("RECARGOS PROPUESTOS (h)",extra,labels,0xFFEB8D56);
  int p=4,c=5;
  String d=days[c]>=days[p]?"+":"";
  body.addView(mtText("COMPARACIÓN CON EL MES ANTERIOR",14,mtGold(),true));
  body.addView(mtText("Asistencias: "+days[p]+" → "+days[c]+" ("+d+(days[c]-days[p])+")"+
   "\nFichadas: "+marks[p]+" → "+marks[c]+
   "\nHoras comunes estimadas: "+common[p]+" h → "+common[c]+" h"+
   "\nRecargos propuestos: "+extra[p]+" h → "+extra[c]+" h",13,Color.WHITE,false));
  body.addView(mtText("El gráfico se basa en fichadas guardadas y controles horarios, no en salarios ni horas aprobadas. Los períodos anteriores sin archivo importado muestran cero registros.",11,mtPale(),false));
 }
 // Add separate totals page to exported PDF when report includes the whole plantel.
 void h79PdfTotals(android.graphics.pdf.PdfDocument pdf,android.graphics.Paint paint,String from,String to,String pid,int pageNo){
  long[] n=h79AllTotals(from,to,pid);
  android.graphics.pdf.PdfDocument.Page pg=pdf.startPage(new android.graphics.pdf.PdfDocument.PageInfo.Builder(595,842,pageNo).create());
  android.graphics.Canvas cv=pg.getCanvas();
  hrPdfHeader(cv,paint,from,to,pageNo,pid==null?"RESUMEN GENERAL":"RESUMEN INDIVIDUAL");
  String[] labels={"PERSONAS CON FICHADAS","DÍAS CON ASISTENCIA","MARCACIONES TOTALES","HORAS ENTRE MARCAS VÁLIDAS","HORAS COMUNES ESTIMADAS","RECARGOS PROPUESTOS","DÍAS CON INCIDENCIAS","TURNOS PROGRAMADOS"};
  String[] vals={""+n[7],""+n[0],""+n[1],hrTime((int)n[2]),hrTime((int)n[3]),hrTime((int)n[4]),""+n[5],""+n[6]};
  int y=230;
  for(int i=0;i<labels.length;i++){
   if(i%2==0){paint.setColor(0xFFEAF3F8);cv.drawRect(30,y-25,560,y+15,paint);}
   hrPdfText(cv,paint,labels[i],36,y,12,0xFF12354D);
   hrPdfText(cv,paint,vals[i],405,y,17,0xFF124F44);
   y+=53;
  }
  hrPdfText(cv,paint,"Indicadores estimados; recargos sin aprobar.",34,680,11,0xFF794D11);
  hrPdfText(cv,paint,"Sin costos ni importes salariales.",34,707,11,0xFF794D11);
  hrPdfFooter(cv,paint,pageNo);pdf.finishPage(pg);
 }
'''
assert ' void dualClockHub(){' in s
s=s.replace(' void dualClockHub(){',extra+'\n void dualClockHub(){',1)
# Entire plantel screen gets grand totals directly after all employee rows.
needle='''  body.addView(mtText("Cifras orientativas: la tolerancia no genera recargo. El recargo calculado NO está aprobado para liquidación. REVISAR marcas incompletas, pausas y horarios nocturnos. Nunca se calculan importes.",11,mtPale(),false));'''
assert needle in s
s=s.replace(needle,'''  h79TotalsPanel(from,to);
'''+needle,1)
# Employee chart in existing individual time control and salary preparation.
anchor='''  body.addView(mtText("Jornada común: "+rule[0]+" - "+rule[1]+" · Tolerancia: "+rule[2]+" min (entrada/salida)",12,mtPale(),false));'''
assert anchor in s
s=s.replace(anchor,anchor+'\n  h79EmployeeCharts(pid,from);',1)
individual='''  body.addView(mtText(person+" · "+from+" — "+to,17,Color.WHITE,true));'''
assert individual in s
s=s.replace(individual,individual+'\n  h79EmployeeCharts(pid,from);',1)
# Summary page at the end of every PDF; the PDF remains internally self-contained.
pdfneedle='''   hrPdfFooter(canvas,paint,pageNo);pdf.finishPage(page);
   java.io.ByteArrayOutputStream out=new java.io.ByteArrayOutputStream();'''
assert pdfneedle in s
s=s.replace(pdfneedle,'''   hrPdfFooter(canvas,paint,pageNo);pdf.finishPage(page);
   h79PdfTotals(pdf,paint,from,to,pid,pageNo+1);
   java.io.ByteArrayOutputStream out=new java.io.ByteArrayOutputStream();''',1)
p.write_text(s)
print("V79 compiled source includes grand totals per plantel and PDF, employee six-month colored bars and comparison")
