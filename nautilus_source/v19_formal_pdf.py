from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 void generateFormalPdf(){
  try{
   android.graphics.pdf.PdfDocument doc=new android.graphics.pdf.PdfDocument();android.graphics.pdf.PdfDocument.PageInfo info=new android.graphics.pdf.PdfDocument.PageInfo.Builder(595,842,1).create();android.graphics.pdf.PdfDocument.Page page=doc.startPage(info);Canvas c=page.getCanvas();Paint paint=new Paint(1);
   paint.setColor(Color.rgb(8,28,39));c.drawRect(0,0,595,842,paint);paint.setColor(Color.rgb(244,190,46));c.drawRect(0,0,595,8,paint);
   paint.setColor(Color.WHITE);paint.setTextSize(24);paint.setFakeBoldText(true);c.drawText("NAUTILUS COUNTRY",40,58,paint);paint.setTextSize(12);paint.setFakeBoldText(false);paint.setLetterSpacing(.08f);c.drawText("P R E S E N T I S M O",40,80,paint);
   paint.setColor(Color.rgb(244,190,46));paint.setTextSize(18);c.drawText("INFORME MENSUAL",40,125,paint);paint.setColor(Color.rgb(190,210,218));paint.setTextSize(11);c.drawText("Período: "+selectedYm+"    Emisión: "+new SimpleDateFormat("dd/MM/yyyy HH:mm",Locale.US).format(new Date()),40,146,paint);
   int y=190;paint.setTextSize(12);paint.setColor(Color.WHITE);paint.setFakeBoldText(true);c.drawText("DETALLE POR SECTOR",40,y,paint);paint.setFakeBoldText(false);y+=28;
   Cursor sc=db.getReadableDatabase().rawQuery("SELECT name FROM sectors ORDER BY name",null);while(sc.moveToNext()&&y<735){String sec=sc.getString(0);int[] z=sectorCoverageToday(sec);paint.setColor(Color.rgb(18,48,60));c.drawRoundRect(40,y-17,555,y+18,8,8,paint);paint.setColor(Color.WHITE);paint.setTextSize(12);c.drawText(sec,55,y+5,paint);paint.setColor(z[1]==0||z[0]>=z[1]?Color.rgb(48,205,166):Color.rgb(235,82,82));paint.setFakeBoldText(true);c.drawText(z[0]+"/"+z[1],500,y+5,paint);paint.setFakeBoldText(false);y+=45;}sc.close();
   paint.setColor(Color.rgb(150,175,185));paint.setTextSize(9);c.drawText("Nautilus Country · Documento generado por Presentismo",40,810,paint);doc.finishPage(page);
   java.io.File dir=new java.io.File(getExternalFilesDir(null),"informes");dir.mkdirs();String stamp=new SimpleDateFormat("yyyyMMdd-HHmmss",Locale.US).format(new Date());java.io.File out=new java.io.File(dir,"Nautilus-Presentismo-"+selectedYm+"-"+stamp+".pdf");java.io.FileOutputStream fos=new java.io.FileOutputStream(out);doc.writeTo(fos);fos.close();doc.close();toast("PDF generado: "+out.getName());
  }catch(Exception e){toast("No se pudo generar PDF: "+e.getMessage());}
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Route every formal PDF reference to the real generator.
s=s.replace('addRefRow("▤","Generar PDF","Informe formal de Nautilus Country","›",Color.rgb(235,82,82),this::monthClose);','addRefRow("▤","Generar PDF","Informe formal de Nautilus Country","›",Color.rgb(235,82,82),this::generateFormalPdf);')
s=s.replace('btn("GENERAR PDF",this::monthClose);','btn("GENERAR PDF",this::generateFormalPdf);')
s=s.replace('V18 HARDENED','V19 REPORTING')
p.write_text(s)
print("V19 formal PDF reporting applied")
