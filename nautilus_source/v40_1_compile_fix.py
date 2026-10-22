from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
old='btn("COMPARTIR",()->shareText("Nautilus Country · "+(month?"Informe mensual ":"Informe semanal ")+from+" a "+to+"\\nDiagramados: "+scheduled+" · Asistencias: "+worked+" · Ausencias: "+abs+" · Tardanzas: "+late))'
new='btn("COMPARTIR",()->{ Intent sh=new Intent(Intent.ACTION_SEND); sh.setType("text/plain"); sh.putExtra(Intent.EXTRA_TEXT,"Nautilus Country · "+(month?"Informe mensual ":"Informe semanal ")+from+" a "+to+"\\nDiagramados: "+scheduled+" · Asistencias: "+worked+" · Ausencias: "+abs+" · Tardanzas: "+late); startActivity(Intent.createChooser(sh,"Compartir informe")); })'
assert old in s
p.write_text(s.replace(old,new).replace("V40 QUICK REPORT CORE","V40.1 QUICK REPORT COMPILE FIX"))
print("V40.1 share compile fix applied")
