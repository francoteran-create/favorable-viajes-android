#!/usr/bin/env bash
set -euo pipefail
mkdir -p out/smoke
snap(){ adb shell uiautomator dump "/sdcard/$1.xml" >/dev/null; adb pull "/sdcard/$1.xml" "out/smoke/$1.xml" >/dev/null; }
click(){ local xy; xy="$(python3 nautilus_source/ci_android_tap.py "out/smoke/$1.xml" "$2")"; adb shell input tap $xy; }
click logs_import_result "ACEPTAR"
sleep 2
snap reports_from_import
click reports_from_import "INFORMES"
sleep 2
snap reports_pdf_entry
grep -F -q "PDF MENSUAL" out/smoke/reports_pdf_entry.xml
click reports_pdf_entry "PDF MENSUAL"
sleep 2
snap select_pdf_month
grep -F -q "OCTUBRE 2026" out/smoke/select_pdf_month.xml
click select_pdf_month "OCTUBRE 2026"
sleep 3
snap system_pdf_picker
grep -F -q "Nautilus-Mensual-2026-10" out/smoke/system_pdf_picker.xml
echo "PASS: October monthly PDF generated and Android Save As picker launched" | tee out/smoke/pdf_result.txt
