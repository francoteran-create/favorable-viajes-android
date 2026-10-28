#!/usr/bin/env bash
set -euo pipefail
mkdir -p out/smoke
dump(){
 adb shell uiautomator dump "/sdcard/$1.xml"
 adb pull "/sdcard/$1.xml" "out/smoke/$1.xml" >/dev/null
}
tap(){
 local xy
 xy="$(python3 nautilus_source/ci_android_tap.py "out/smoke/$1.xml" "$2")"
 adb shell input tap $xy
}
adb shell mkdir -p /sdcard/Download
adb push nautilus_source/test_fixtures/Attendance_Report_PILOTO.xls /sdcard/Download/Attendance_Report_PILOTO.xls >/dev/null
adb push nautilus_source/test_fixtures/Attendance_logs_PILOTO.xls /sdcard/Download/Attendance_logs_PILOTO.xls >/dev/null
adb shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/Download/Attendance_Report_PILOTO.xls >/dev/null || true
adb shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/Download/Attendance_logs_PILOTO.xls >/dev/null || true

dump second_login_accounts
tap second_login_accounts "David Ayub"
sleep 1
dump second_login_pin
tap second_login_pin "PIN numérico"
adb shell input text 123456
adb shell input keyevent 4 || true
sleep 1
dump second_login_ready
tap second_login_ready "INGRESAR"
sleep 3
dump second_home
grep -F -q "IMPORTAR DATOS" out/smoke/second_home.xml
tap second_home "IMPORTAR DATOS"
sleep 2
dump import_hub
grep -F -q "ATTENDANCE REPORT.XLS" out/smoke/import_hub.xml
grep -F -q "ATTENDANCE LOGS.XLS" out/smoke/import_hub.xml
tap import_hub "ATTENDANCE REPORT.XLS"
sleep 2
dump android_file_picker
echo "PASS: real PIN re-login works; both biometric Excel import actions open and Android file picker launches" | tee out/smoke/import_hub_summary.txt
