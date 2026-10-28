from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
m=re.search(r"\bvoid\s+generateFormalPdf\s*\(\s*\)\s*\{",s)
assert m,"Formal PDF method is missing"
start=m.start()
brace=s.index("{",m.start())
depth=0
quote=None
escaped=False
end=None
for index in range(brace,len(s)):
    ch=s[index]
    if quote is not None:
        if escaped:escaped=False
        elif ch=="\\":escaped=True
        elif ch==quote:quote=None
        continue
    if ch in ("'",'"'):quote=ch;continue
    if ch=="{":depth+=1
    elif ch=="}":
        depth-=1
        if depth==0:
            end=index+1
            break
assert end is not None
old=s[start:end]
assert "sectorCoverageToday" in old,"Older misleading today-based PDF changed"
new=r'''void generateFormalPdf(){
  // A monthly PDF must reflect the selected month's scheduled days and punches.
  // The original version incorrectly displayed today's sector coverage.
  android.graphics.pdf.PdfDocument pdf=new android.graphics.pdf.PdfDocument();
  try{
   String ym=selectedYm;
   if(ym==null||!ym.matches("\\d{4}-(0[1-9]|1[0-2])"))
    throw new java.io.IOException("Seleccioná un mes válido antes de exportar");
   java.text.SimpleDateFormat date=new java.text.SimpleDateFormat("yyyy-MM-dd",Locale.US);
   date.setLenient(false);
   java.util.Calendar cal=java.util.Calendar.getInstance();
   cal.setTime(date.parse(ym+"-01"));
   String from=ym+"-01";
   cal.add(java.util.Calendar.MONTH,1);
   cal.add(java.util.Calendar.DAY_OF_MONTH,-1);
   String to=date.format(cal.getTime());
   android.graphics.Paint paint=new android.graphics.Paint(1);
   int pages=j81PdfSummary(pdf,paint,from,to,null,0);
   if(pages<1)throw new java.io.IOException("El informe no generó páginas");
   java.io.File root=getExternalFilesDir(null);
   if(root==null)throw new java.io.IOException("Almacenamiento del teléfono no disponible");
   java.io.File folder=new java.io.File(root,"informes");
   if(!folder.exists()&&!folder.mkdirs())throw new java.io.IOException("No se pudo crear la carpeta de informes");
   String stamp=new SimpleDateFormat("yyyyMMdd-HHmmss",Locale.US).format(new Date());
   java.io.File out=new java.io.File(folder,"Nautilus-Mensual-"+ym+"-"+stamp+".pdf");
   try(java.io.FileOutputStream fos=new java.io.FileOutputStream(out)){
    pdf.writeTo(fos);
   }
   toast("PDF mensual generado ("+pages+" páginas): "+out.getName());
  }catch(Exception e){toast("No se pudo generar PDF: "+e.getMessage());}
  finally{pdf.close();}
 }'''
s=s[:start]+new+s[end:]
p.write_text(s)
print("V110 monthly PDF now uses selected period, per-employee jornadas and general totals, not today's sector coverage")
