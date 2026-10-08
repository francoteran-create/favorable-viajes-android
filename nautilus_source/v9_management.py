from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
marker=" void sectorStats(){"
assert marker in s
code=r"""
 void managementSummary(){
  base("CONTROL DE PERSONAL");
  body.addView(muted("Indicadores para gestión · mes actual"));
  btn("ESTADÍSTICAS POR TRABAJADOR",this::workerStats);
  btn("ESTADÍSTICAS POR SECTOR",this::sectorStats);
  btn("RANKING DEL PERSONAL",this::workerRanking);
  btn("INCIDENCIAS PENDIENTES",this::reviews);
  btn("RESUMEN PARA LIQUIDACIÓN",this::payrollSummary);
  btn("CIERRE MENSUAL",this::monthClose);
 }
"""
s=s.replace(marker,code+"\n"+marker)
s=s.replace('void statsHub(){','void statsHub(){')
s=s.replace('btn("ESTADÍSTICAS · PERSONAL Y SECTORES",this::statsHub);','btn("CONTROL Y ESTADÍSTICAS",this::managementSummary);')
p.write_text(s)

# V9 compatibility with the proven V6 attendance engine
s=p.read_text()
if 'String currentScreen=' not in s:
 s=s.replace('static final int PICK=12, SAVE_REPORT=13;','static final int PICK=12, SAVE_REPORT=13; String currentScreen="HOY";')
s=s.replace('dayResult(pid,day)','calcDay(pid,day)')
s=s.replace('dayResult(pid,String.format(Locale.US,"%s-%02d",ym,d))','calcDay(pid,String.format(Locale.US,"%s-%02d",ym,d))')
s=s.replace('r.present','r.worked>0')
s=s.replace('r.lateMinutes','r.late')
s=s.replace('r.clockMinutes','r.worked')
# recognized minute display falls back to worked minutes in analytics; review-aware payroll remains untouched
s=s.replace('r.recognizedMinutes','r.worked')
p.write_text(s)
print("V9 embedded compatibility applied")

# V10 visual rebuild is applied by importing/running the dedicated transformer
import runpy
runpy.run_path(str(Path(__file__).with_name("v10_visual_rebuild.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v105_visual_structure.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v11_profiles_reports.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v12_reference_fidelity.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v13_core_reference_screens.py")),run_name="__main__")
