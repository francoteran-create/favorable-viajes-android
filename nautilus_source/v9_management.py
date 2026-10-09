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

runpy.run_path(str(Path(__file__).with_name("v35_real_reporting.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v36_more_actions.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v36_1_more_hotfix.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v37_consolidated_flow.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v38_startup_hardening.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v39_runtime_schema_repair.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v40_quick_report_core.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v40_1_compile_fix.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v40_2_compile_fix.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v41_week_planning.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v41_1_visual_compile_fix.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v42_home_skin.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v43_premium_home.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v43_1_compile_fix.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v44_home_summary.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v45_home_day_control.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v46_premium_nav.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v47_unified_modules.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v48_person_photo.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v48_1_release_fix.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v49_safe_boot.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v50_reference_home.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v51_functional_reference.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v52_master_image_home.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v52_1_compile_fix.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v52_2_compile_fix.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v53_master_components_only.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v54_personnel_photo_home.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v55_readable_components.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v55_1_compile_fix.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v56_global_ui_compat.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v56_1_compile_fix.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v57_master_shell.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v58_explicit_menus.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v58_1_compile_fix.py")),run_name="__main__")

runpy.run_path(str(Path(__file__).with_name("v59_cinematic_native_home.py")),run_name="__main__")
