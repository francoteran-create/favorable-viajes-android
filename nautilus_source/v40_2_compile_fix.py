from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
old='sectionTitle("EXPORTAR / COMPARTIR","Salida rápida del informe");btn("EXPORTAR CSV / EXCEL",this::exportCsv);btn("GENERAR PDF",this::reports);btn("COMPARTIR",()->{ Intent sh=new Intent(Intent.ACTION_SEND); sh.setType("text/plain"); sh.putExtra(Intent.EXTRA_TEXT,"Nautilus Country · "+(month?"Informe mensual ":"Informe semanal ")+from+" a "+to+"\\nDiagramados: "+scheduled+" · Asistencias: "+worked+" · Ausencias: "+abs+" · Tardanzas: "+late); startActivity(Intent.createChooser(sh,"Compartir informe")); });exactBottom("INFORMES");'
new='final String quickShare="Nautilus Country · "+(month?"Informe mensual ":"Informe semanal ")+from+" a "+to+"\\nDiagramados: "+scheduled+" · Asistencias: "+worked+" · Ausencias: "+abs+" · Tardanzas: "+late; sectionTitle("EXPORTAR / COMPARTIR","Salida rápida del informe");btn("EXPORTAR CSV / EXCEL",this::exportCsv);btn("GENERAR PDF",this::reports);btn("COMPARTIR",()->{ Intent sh=new Intent(Intent.ACTION_SEND); sh.setType("text/plain"); sh.putExtra(Intent.EXTRA_TEXT,quickShare); startActivity(Intent.createChooser(sh,"Compartir informe")); });exactBottom("INFORMES");'
assert old in s
p.write_text(s.replace(old,new).replace("V40.1 QUICK REPORT COMPILE FIX","V40.2 QUICK REPORT COMPILE FIX"))
print("V40.2 lambda compile fix applied")
