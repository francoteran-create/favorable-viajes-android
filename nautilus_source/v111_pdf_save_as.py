from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark="void generateFormalPdf(){"
assert s.count(mark)==1
s=s.replace(mark,"static final int SAVE_MONTHLY_PDF=915;\n "+mark,1)
mark='''   toast("PDF mensual generado ("+pages+" páginas): "+out.getName());'''
assert s.count(mark)==1
s=s.replace(mark,'''   // Also let the user export the PDF outside the app-private folder.
   getSharedPreferences("nautilus_exports",MODE_PRIVATE).edit()
     .putString("monthly_pdf_pending",out.getAbsolutePath()).apply();
   Intent save=new Intent(Intent.ACTION_CREATE_DOCUMENT);
   save.addCategory(Intent.CATEGORY_OPENABLE);
   save.setType("application/pdf");
   save.putExtra(Intent.EXTRA_TITLE,out.getName());
   startActivityForResult(save,SAVE_MONTHLY_PDF);
''',1)
m=re.search(r"\bvoid\s+onActivityResult\s*\(\s*int\s+(\w+)\s*,\s*int\s+(\w+)\s*,\s*Intent\s+(\w+)\s*\)\s*\{",s)
assert m,"activity result callback missing"
q,r,d=m.groups()
handler=f'''if({q}==SAVE_MONTHLY_PDF){{
   if({r}==RESULT_OK&&{d}!=null&&{d}.getData()!=null){{
    try{{
     String path=getSharedPreferences("nautilus_exports",MODE_PRIVATE).getString("monthly_pdf_pending","");
     if(path.isEmpty())throw new java.io.IOException("No hay informe pendiente para guardar");
     java.io.File original=new java.io.File(path);
     java.io.File base=getExternalFilesDir(null);
     if(base==null||!original.getCanonicalPath().startsWith(base.getCanonicalPath()+java.io.File.separator))
      throw new java.io.IOException("El archivo de informe no es válido");
     try(java.io.InputStream in=new java.io.FileInputStream(original);
         java.io.OutputStream out=getContentResolver().openOutputStream({d}.getData())){{
      if(out==null)throw new java.io.IOException("El destino de exportación no está disponible");
      byte[] block=new byte[8192];int n;
      while((n=in.read(block))!=-1)out.write(block,0,n);
     }}
     msg("PDF GUARDADO","Informe mensual exportado correctamente. Ya podés compartirlo desde la carpeta que elegiste.",this::reports);
    }}catch(Exception ex){{msg("No se pudo guardar el PDF",ex.getMessage(),this::reports);}}
   }}else toast("El PDF se conserva dentro de Nautilus. Podés volver a generarlo para exportarlo.");
   return;
  }}'''
s=s[:m.end()]+handler+s[m.end():]
p.write_text(s)
print("V111: monthly PDF uses Android Save As document picker and copies the exact generated PDF to chosen folder")
