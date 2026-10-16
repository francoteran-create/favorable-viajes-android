from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void dualClockHub(){'
assert mark in s
java=r'''
 // PDF: first each employee's jornada overview, then the grand total, then raw daily punch details.
 int j81PdfSummary(android.graphics.pdf.PdfDocument pdf,android.graphics.Paint paint,String from,String to,String pid,int lastPage){
  rsEnsure();
  int pageNo=lastPage, y=0;
  android.graphics.pdf.PdfDocument.Page page=null;
  android.graphics.Canvas canvas=null;
  long[] all=new long[8];int employeeCount=0;
  Cursor staff=db.getReadableDatabase().rawQuery(
   "SELECT id,COALESCE(NULLIF(name,''),id) FROM people WHERE active=1 "+(pid==null?"":"AND id=? ")+"ORDER BY name",
   pid==null?null:new String[]{pid});
  try{while(staff.moveToNext()){
   String personId=staff.getString(0),name=staff.getString(1);
   long[] n=j80Counts(personId,from,to);
   employeeCount++;for(int k=0;k<8;k++)all[k]+=n[k];
   if(page==null || y>695){
    if(page!=null){hrPdfFooter(canvas,paint,pageNo);pdf.finishPage(page);}
    pageNo++;
    page=pdf.startPage(new android.graphics.pdf.PdfDocument.PageInfo.Builder(595,842,pageNo).create());
    canvas=page.getCanvas();
    hrPdfHeader(canvas,paint,from,to,pageNo,"JORNADAS POR EMPLEADO");
    hrPdfText(canvas,paint,"RESUMEN DE JORNADAS · TODOS LOS EMPLEADOS",30,201,13,0xFF12354D);
    y=231;
   }
   if(employeeCount%2==0){paint.setColor(0xFFEAF3F8);canvas.drawRect(28,y-17,567,y+55,paint);}
   hrPdfText(canvas,paint,name,34,y,12,0xFF12354D);
   hrPdfText(canvas,paint,"Programadas "+n[0]+"  |  Con fichadas "+n[1]+"  |  Sin fichar "+n[2]+"  |  Francos "+n[3],34,y+19,10,0xFF124F44);
   hrPdfText(canvas,paint,"Revisar "+n[4]+"  |  Marcas "+n[5]+"  |  Comunes "+hrTime((int)n[6])+"  |  Recargos "+hrTime((int)n[7]),34,y+38,10,0xFF794D11);
   y+=76;
  }}finally{staff.close();}
  if(page!=null){hrPdfFooter(canvas,paint,pageNo);pdf.finishPage(page);}
  pageNo++;
  page=pdf.startPage(new android.graphics.pdf.PdfDocument.PageInfo.Builder(595,842,pageNo).create());
  canvas=page.getCanvas();
  hrPdfHeader(canvas,paint,from,to,pageNo,"TOTAL GENERAL DEL PLANTEL");
  hrPdfText(canvas,paint,"TOTAL GENERAL DEL PLANTEL",30,203,18,0xFF12354D);
  String[] labels={"Empleados","Jornadas programadas","Jornadas con fichadas","Programadas sin fichar (revisar)","Francos","Dias con marcas incompletas","Marcaciones totales","Horas comunes estimadas","Recargos propuestos"};
  String[] values={""+employeeCount,""+all[0],""+all[1],""+all[2],""+all[3],""+all[4],""+all[5],hrTime((int)all[6]),hrTime((int)all[7])};
  int lineY=250;
  for(int i=0;i<labels.length;i++){
   if(i%2==0){paint.setColor(0xFFEAF3F8);canvas.drawRect(29,lineY-21,560,lineY+18,paint);}
   hrPdfText(canvas,paint,labels[i],35,lineY,12,0xFF12354D);
   hrPdfText(canvas,paint,values[i],442,lineY,16,0xFF124F44);
   lineY+=45;
  }
  hrPdfText(canvas,paint,"Con fichadas no equivale a jornada completa validada.",34,695,10,0xFF794D11);
  hrPdfText(canvas,paint,"Sin fichar no equivale a ausencia confirmada. Recargos sin aprobar.",34,715,10,0xFF794D11);
  hrPdfFooter(canvas,paint,pageNo);pdf.finishPage(page);
  return pageNo;
 }
'''
s=s.replace(mark,java+'\n'+mark,1)
needle='''  try{
   String sql="SELECT id,COALESCE(NULLIF(name,''),id) FROM people WHERE active=1 "+(pid==null?"":"AND id=? ")+"ORDER BY name";'''
assert needle in s, "PDF method structure changed"
s=s.replace(needle,'''  try{
   pageNo=j81PdfSummary(pdf,paint,from,to,pid,pageNo);
   String sql="SELECT id,COALESCE(NULLIF(name,''),id) FROM people WHERE active=1 "+(pid==null?"":"AND id=? ")+"ORDER BY name";''',1)
# V79 placed the totals at end: now summary and totals are already at front.
assert '   h79PdfTotals(pdf,paint,from,to,pid,pageNo+1);' in s
s=s.replace('   h79PdfTotals(pdf,paint,from,to,pid,pageNo+1);','',1)
p.write_text(s)
print("V81 PDF: employee jornadas -> grand totals -> detailed daily records")
