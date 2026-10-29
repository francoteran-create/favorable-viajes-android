from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
needle='''   int pages=j81PdfSummary(pdf,paint,from,to,null,0);'''
assert needle in s,"PDF summary invocation changed"
s=s.replace(needle,'''   int pages=j115ReadablePdf(pdf,paint,from,to);''',1)
anchor=' void generateFormalPdf(){'
assert anchor in s
java=r'''
 int j115ReadablePdf(android.graphics.pdf.PdfDocument doc,android.graphics.Paint pen,String from,String to){
  rsEnsure();
  java.util.ArrayList<String> names=new java.util.ArrayList<>();
  java.util.ArrayList<long[]> records=new java.util.ArrayList<>();
  long[] grand=new long[8];
  Cursor people=db.getReadableDatabase().rawQuery(
   "SELECT id,COALESCE(NULLIF(name,''),id) FROM people WHERE active=1 ORDER BY name",null);
  try{
   while(people.moveToNext()){
    String id=people.getString(0),name=people.getString(1);
    long[] n=j80Counts(id,from,to);
    names.add(name);records.add(n);
    for(int i=0;i<8;i++)grand[i]+=n[i];
   }
  }finally{people.close();}
  int pageNo=0,perPage=6;
  for(int offset=0;offset<names.size()||offset==0;offset+=perPage){
   pageNo++;
   android.graphics.pdf.PdfDocument.Page pg=doc.startPage(
    new android.graphics.pdf.PdfDocument.PageInfo.Builder(595,842,pageNo).create());
   android.graphics.Canvas c=pg.getCanvas();
   j115Header(c,pen,"JORNADAS POR EMPLEADO",from,to,pageNo);
   int y=165;
   if(names.isEmpty())j115Text(c,pen,"Sin empleados activos para informar",40,200,13,0xFF263F50,true);
   for(int i=offset;i<Math.min(names.size(),offset+perPage);i++){
    long[] n=records.get(i);
    pen.setColor(i%2==0?0xFFE9F2F7:0xFFF5F9FB);
    c.drawRoundRect(30,y-8,565,y+84,10,10,pen);
    String name=names.get(i);
    pen.setTypeface(android.graphics.Typeface.create("sans-serif",android.graphics.Typeface.BOLD));
    pen.setTextSize(15);
    while(name.length()>1&&pen.measureText(name)>480)name=name.substring(0,name.length()-2)+"…";
    j115Text(c,pen,name,43,y+15,15,0xFF193D52,true);
    j115Text(c,pen,"Programadas: "+n[0]+"     Con fichadas: "+n[1]+"     Sin fichar: "+n[2]+"     Francos: "+n[3],43,y+39,11,0xFF315265,false);
    j115Text(c,pen,"Revisar: "+n[4]+"     Marcaciones: "+n[5]+"     Comunes: "+hrTime((int)n[6])+"     Recargos: "+hrTime((int)n[7]),43,y+60,11,0xFF315265,false);
    y+=107;
   }
   j115Footer(c,pen,pageNo);
   doc.finishPage(pg);
  }
  pageNo++;
  android.graphics.pdf.PdfDocument.Page pg=doc.startPage(
   new android.graphics.pdf.PdfDocument.PageInfo.Builder(595,842,pageNo).create());
  android.graphics.Canvas c=pg.getCanvas();
  j115Header(c,pen,"TOTAL GENERAL DEL PLANTEL",from,to,pageNo);
  String[] labels={"Empleados activos","Jornadas programadas","Dias con fichadas","Programadas sin fichar - revisar",
   "Francos programados","Dias con marcas incompletas","Marcaciones del reloj","Horas comunes estimadas","Recargos propuestos"};
  String[] values={""+names.size(),""+grand[0],""+grand[1],""+grand[2],""+grand[3],""+grand[4],""+grand[5],
   hrTime((int)grand[6]),hrTime((int)grand[7])};
  int y=170;
  for(int i=0;i<labels.length;i++){
   pen.setColor(i%2==0?0xFFE9F2F7:0xFFF5F9FB);
   c.drawRoundRect(32,y-20,563,y+23,7,7,pen);
   j115Text(c,pen,labels[i],45,y+5,12,0xFF243E51,false);
   j115Text(c,pen,values[i],470,y+5,15,0xFF165D60,true);
   y+=52;
  }
  j115Text(c,pen,"Con fichadas no significa jornada completa validada.",38,687,11,0xFF6F5430,false);
  j115Text(c,pen,"Sin fichar no equivale a ausencia confirmada.",38,705,11,0xFF6F5430,false);
  j115Text(c,pen,"Recargos propuestos: no aprobados para liquidacion.",38,723,11,0xFF6F5430,false);
  j115Footer(c,pen,pageNo);
  doc.finishPage(pg);
  return pageNo;
 }
 void j115Text(android.graphics.Canvas c,android.graphics.Paint p,String t,int x,int y,int size,int color,boolean bold){
  p.setColor(color);p.setTextSize(size);
  p.setTypeface(android.graphics.Typeface.create("sans-serif",bold?android.graphics.Typeface.BOLD:android.graphics.Typeface.NORMAL));
  c.drawText(t,x,y,p);
 }
 void j115Header(android.graphics.Canvas c,android.graphics.Paint p,String label,String from,String to,int page){
  p.setColor(0xFF0C2B3B);c.drawRect(0,0,595,129,p);
  p.setColor(0xFFD8AC3A);c.drawRect(0,0,595,7,p);
  j115Text(c,p,"NAUTILUS COUNTRY",33,49,22,0xFFFFFFFF,true);
  j115Text(c,p,"PRESENTISMO - INFORME MENSUAL",33,75,12,0xFFE6B74A,true);
  j115Text(c,p,label,33,108,16,0xFFFFFFFF,true);
  j115Text(c,p,"Periodo: "+from+" al "+to,33,148,11,0xFF34576A,false);
 }
 void j115Footer(android.graphics.Canvas c,android.graphics.Paint p,int page){
  p.setColor(0xFFDEE8EC);c.drawRect(30,778,565,780,p);
  j115Text(c,p,"Nautilus Presentismo  |  Control interno, no liquidacion salarial",32,801,10,0xFF54707D,false);
  j115Text(c,p,"Pagina "+page,505,801,10,0xFF54707D,false);
 }
'''
s=s.replace(anchor,java+"\n"+anchor,1)
p.write_text(s)
print("V115: clean paginated A4 reports, individual full-width cards and legible monthly grand totals")
