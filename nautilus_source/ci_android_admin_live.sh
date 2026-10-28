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
dump owner_after_roster
grep -q "DESARROLLADOR" out/smoke/owner_after_roster.xml
tap owner_after_roster "VOLVER"
sleep 2
dump choose_admin_live
tap choose_admin_live "David Ayub"
sleep 2
dump first_admin_pin_live
grep -F -q "PRIMER INGRESO" out/smoke/first_admin_pin_live.xml
tap first_admin_pin_live "Crear PIN (4 a 6 números)"
adb shell input text 123456
sleep 1
dump first_pin_entered
tap first_pin_entered "Repetir PIN"
adb shell input text 123456
sleep 1
adb shell input keyevent 4 || true
dump ready_to_create_pin
tap ready_to_create_pin "CREAR"
sleep 4
dump admin_main_live
if ! grep -F -q "CAMBIAR DE USUARIO" out/smoke/admin_main_live.xml; then
  echo "::error::Account creation did not reach the presentismo home with change-user action"
  exit 1
fi
if grep -F -q "VOLVER AL PANEL DESARROLLADOR" out/smoke/admin_main_live.xml; then
  echo "::error::Administrator was shown the exclusive owner panel shortcut"
  exit 1
fi
tap admin_main_live "CAMBIAR DE USUARIO"
sleep 2
dump after_switch_live
grep -F -q "DESARROLLADOR" out/smoke/after_switch_live.xml
grep -F -q "Enzo Ahumada" out/smoke/after_switch_live.xml
adb logcat -d -b crash > out/smoke/admin_login_crashes.txt
if grep -F -q "Process: ar.com.nautiluscountry.presentismo" out/smoke/admin_login_crashes.txt; then
  echo "::error::Nautilus crashed during real PIN login and user switching"
  exit 1
fi
echo "PASS: fresh administrator PIN created; home and account switch visible; exclusive developer panel hidden; session changed safely" | tee out/smoke/admin_live_summary.txt
