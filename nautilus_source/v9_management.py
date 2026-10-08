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

runpy.run_path(str(Path(__file__).with_name("v14_reports_incidents_more.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v15_compile_cleanup.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v16_nuclear_fidelity.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v17_reactor_operational.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v18_backup_hardening.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v19_formal_pdf.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v20_compile_repair.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v21_compile_hardening.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v22_visual_reactor.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v23_visual_fusion.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v24_calendar_people.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v25_diagram_roster.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v26_personnel_master.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v27_touch_calendar.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v27_1_startup_hotfix.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v28_exact_8screens.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v29_exact_reference_content.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v30_exact_navigation.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v31_live_data.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v32_dynamic_turns.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v33_employee_month.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v34_personal_report.py")),run_name="__main__")
