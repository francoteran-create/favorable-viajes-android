from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# V20 build repair: project uses msg(), not toast().
s=s.replace('toast("Todavía no existe base para copiar")','msg("Todavía no existe base para copiar")')
s=s.replace('toast("Backup creado: "+dst.getName())','msg("Backup creado: "+dst.getName())')
s=s.replace('toast("No se pudo crear backup: "+e.getMessage())','msg("No se pudo crear backup: "+e.getMessage())')
s=s.replace('toast("No se pudo abrir el backup")','msg("No se pudo abrir el backup")')
s=s.replace('toast("Backup restaurado")','msg("Backup restaurado")')
s=s.replace('toast("No se pudo restaurar: "+e.getMessage())','msg("No se pudo restaurar: "+e.getMessage())')
s=s.replace('toast("PDF generado: "+out.getName())','msg("PDF generado: "+out.getName())')
s=s.replace('toast("No se pudo generar PDF: "+e.getMessage())','msg("No se pudo generar PDF: "+e.getMessage())')
# Avoid selectedYm dependency in PDF; derive current month locally.
s=s.replace('"Período: "+selectedYm+"    Emisión: "', '"Período: "+new SimpleDateFormat("yyyy-MM",Locale.US).format(new Date())+"    Emisión: "')
s=s.replace('"Nautilus-Presentismo-"+selectedYm+"-"+stamp+".pdf"', '"Nautilus-Presentismo-"+new SimpleDateFormat("yyyy-MM",Locale.US).format(new Date())+"-"+stamp+".pdf"')
s=s.replace('V19 REPORTING','V20 MASTER CANDIDATE')
p.write_text(s)
print("V20 compile repair applied")
