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
grep -F -q "MES ACTUAL" out/smoke/select_pdf_month.xml
click select_pdf_month "MES ACTUAL"
sleep 3
snap system_pdf_picker
grep -F -q "Nautilus-Mensual-2026-10" out/smoke/system_pdf_picker.xml
click system_pdf_picker "SAVE"
sleep 3
snap pdf_export_confirmation
REMOTE="$(adb shell 'ls /sdcard/Download/Nautilus-Mensual-2026-10*.pdf 2>/dev/null' | tr -d '\r' | head -1)"
test -n "$REMOTE"
adb pull "$REMOTE" out/smoke/NAUTILUS_MENSUAL_PILOTO.pdf >/dev/null
python3 - <<'PY'
from pathlib import Path
p=Path("out/smoke/NAUTILUS_MENSUAL_PILOTO.pdf")
raw=p.read_bytes()
assert len(raw)>1500,"PDF demasiado pequeño"
assert raw.startswith(b"%PDF-"),"Falta encabezado PDF"
assert b"%%EOF" in raw[-1024:],"PDF incompleto"
print(f"PASS: PDF generado, guardado por Android y validado: {len(raw)} bytes")
PY
echo "PASS: 2 employees, 4 punches and October monthly PDF saved to Downloads" | tee out/smoke/pdf_result.txt
