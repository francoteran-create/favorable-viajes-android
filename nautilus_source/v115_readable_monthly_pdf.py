from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
match=re.search(r'\bint\s+j81PdfSummary\s*\(',s)
assert match,"monthly PDF summary not found"
start=match.start()
opening=s.find("{",start)
assert opening>=0
depth=0
quote=None
escape=False
end=None
for i in range(opening,len(s)):
 ch=s[i]
 if quote:
  if escape:escape=False
  elif ch=="\\":escape=True
  elif ch==quote:quote=None
  continue
 if ch in ("'",'"'):quote=ch;continue
 if ch=="{":depth+=1
 elif ch=="}":
  depth-=1
  if depth==0:
   end=i+1
   break
assert end is not None
new=r'''
 void v115PdfText(android.graphics.Canvas cv,android.graphics.Paint p,String raw,
    float x,float y,float width,float size,int color,boolean bold){
  p.setColor(color);
  p.setStyle(android.graphics.Paint.Style.FILL);
  p.setTypeface(android.graphics.Typeface.create("sans-serif",bold?
     android.graphics.Typeface.BOLD:android.graphics.Typeface.NORMAL));
  p.setTextSize(size);
  String text=raw==null?"":raw;
  while(p.measureText(text)>width&&p.getTextSize()>9f)p.setTextSize(p.getTextSize()-.5f);
  cv.drawText(text,x,y,p);
 }
 void v115PdfFrame(android.graphics.Canvas cv,android.graphics.Paint p,
     String from,String to,int pageNo,String heading){
  p.setColor(0xFF092B40);cv.drawRect(0,0,595,146,p);
  p.setColor(0xFFEFBE50);cv.drawRect(0,146,595,152,p);
  v115PdfText(cv,p,"NAUTILUS COUNTRY",30,55,530,25,0xFFEFBE50,true);
  v115PdfText(cv,p,"PRESENTISMO · INFORME MENSUAL",31,85,525,13,0xFFFFFFFF,true);
  v115PdfText(cv,p,"Período: "+from+" al "+to+"   |   Página "+pageNo,
     31,116,525,11,0xFFDAEAF2,false);
  v115PdfText(cv,p,heading,32,192,530,17,0xFF10364B,true);
  p.setColor(0xFF092B40);cv.drawRect(0,776,595,842,p);
  v115PdfText(cv,p,"Indicadores estimativos. No son una liquidación de haberes.",
      32,804,535,11,0xFFFFFFFF,false);
  v115PdfText(cv,p,"Revisar turnos nocturnos, pausas y marcaciones incompletas.",
      32,826,535,10,0xFFEFBE50,false);
 }
 int j81PdfSummary(android.graphics.pdf.PdfDocument pdf,android.graphics.Paint paint,
   String from,String to,String pid,int lastPage){
  rsEnsure();
  int pageNo=lastPage, workers=0;
  long[] grand=new long[8];
  android.graphics.pdf.PdfDocument.Page page=null;
  android.graphics.Canvas canvas=null;
  int y=0;
  Cursor people=db.getReadableDatabase().rawQuery(
    "SELECT id,COALESCE(NULLIF(name,''),id) FROM people WHERE active=1 "+
      (pid==null?"":"AND id=? ")+"ORDER BY name",
    pid==null?null:new String[]{pid});
  try{
   while(people.moveToNext()){
    String person=people.getString(0),name=people.getString(1);
    long[] n=j80Counts(person,from,to);
    for(int k=0;k<8;k++)grand[k]+=n[k];
    workers++;
    if(page==null||y>680){
     if(page!=null)pdf.finishPage(page);
     pageNo++;
     page=pdf.startPage(new android.graphics.pdf.PdfDocument.PageInfo.Builder(595,842,pageNo).create());
     canvas=page.getCanvas();
     v115PdfFrame(canvas,paint,from,to,pageNo,"JORNADAS POR EMPLEADO");
     y=237;
    }
    paint.setColor(workers%2==0?0xFFE9F2F7:0xFFF5F8FA);
    canvas.drawRoundRect(31,y-22,564,y+59,8,8,paint);
    paint.setColor(0xFF18A57E);canvas.drawRect(31,y-22,36,y+59,paint);
    v115PdfText(canvas,paint,name,46,y,500,15,0xFF17374A,true);
    v115PdfText(canvas,paint,
      "Programadas "+n[0]+"   |   Con fichadas "+n[1]+"   |   Sin fichar "+n[2]+"   |   Francos "+n[3],
      46,y+22,501,11,0xFF175B53,false);
    v115PdfText(canvas,paint,
      "Marcas "+n[5]+"   |   A revisar "+n[4]+"   |   Comunes "+hrTime((int)n[6])+"   |   Recargos "+hrTime((int)n[7]),
      46,y+43,501,11,0xFF7B511C,false);
    y+=91;
   }
  }finally{people.close();}
  if(page==null){
   pageNo++;
   page=pdf.startPage(new android.graphics.pdf.PdfDocument.PageInfo.Builder(595,842,pageNo).create());
   canvas=page.getCanvas();
   v115PdfFrame(canvas,paint,from,to,pageNo,"JORNADAS POR EMPLEADO");
   v115PdfText(canvas,paint,"No hay empleados activos para este informe.",34,251,520,13,0xFF496473,false);
  }
  pdf.finishPage(page);
  pageNo++;
  page=pdf.startPage(new android.graphics.pdf.PdfDocument.PageInfo.Builder(595,842,pageNo).create());
  canvas=page.getCanvas();
  v115PdfFrame(canvas,paint,from,to,pageNo,"TOTAL GENERAL DEL PLANTEL");
  String[] labels={"Empleados","Jornadas programadas","Días con fichadas",
    "Programadas sin fichar (requiere revisión)","Francos programados",
    "Días con marcas a revisar","Marcaciones totales","Horas comunes estimadas",
    "Recargos propuestos (no aprobados)"};
  String[] values={""+workers,""+grand[0],""+grand[1],""+grand[2],""+grand[3],
    ""+grand[4],""+grand[5],hrTime((int)grand[6]),hrTime((int)grand[7])};
  int rowY=242;
  for(int i=0;i<labels.length;i++){
   if(i%2==0){paint.setColor(0xFFE9F2F7);canvas.drawRoundRect(31,rowY-22,564,rowY+17,5,5,paint);}
   v115PdfText(canvas,paint,labels[i],40,rowY,414,12,0xFF17374A,false);
   v115PdfText(canvas,paint,values[i],479,rowY,76,15,0xFF116E61,true);
   rowY+=45;
  }
  v115PdfText(canvas,paint,"Una jornada con fichadas no equivale a jornada completa validada.",
     34,684,525,10,0xFF794D11,false);
  v115PdfText(canvas,paint,"Sin fichar no significa ausencia confirmada; revisar la cobertura del reloj.",
     34,709,525,10,0xFF794D11,false);
  pdf.finishPage(page);
  return pageNo;
 }
'''
s=s[:start]+new+s[end:]
p.write_text(s)
print("V115: rebuilt month PDF with legible full-width row text and clear totals, footer and disclaimer")
