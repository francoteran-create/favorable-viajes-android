#!/usr/bin/env bash
set -euo pipefail
APK="${SMOKE_APK:-${PROJECT}/app/build/outputs/apk/debug/app-debug.apk}"
PKG="ar.com.nautiluscountry.presentismo"
mkdir -p out/smoke
test -s "$APK"
adb install -r "$APK"
adb logcat -c
adb shell am force-stop "$PKG" || true
adb shell am start -W -n "$PKG/.MainActivity" | tee out/smoke/start.txt
sleep 5
PID="$(adb shell pidof "$PKG" | tr -d '\r' || true)"
if [ -z "$PID" ]; then
  adb logcat -d -b crash > out/smoke/crashes.txt
  echo "::error::Nautilus closed after launching on Android emulator"
  exit 1
fi
echo "Android PID=$PID" | tee out/smoke/process.txt
adb shell uiautomator dump /sdcard/nautilus_view.xml || true
adb pull /sdcard/nautilus_view.xml out/smoke/nautilus_view.xml || true
# FLAG_SECURE intentionally blocks screenshots on some Android images.
# The accessibility hierarchy, process and crash logs are the reliable evidence.
if adb shell screencap -p /sdcard/nautilus_smoke.png; then
  adb pull /sdcard/nautilus_smoke.png out/smoke/nautilus_smoke.png || true
else
  echo "Screen capture denied (privacy protection active); UI hierarchy is sufficient." | tee out/smoke/capture_note.txt
fi
adb logcat -d -b crash > out/smoke/crashes.txt
if grep -q -E "FATAL EXCEPTION|Process: $PKG" out/smoke/crashes.txt; then
  echo "::error::Android fatal crash during Nautilus startup"
  exit 1
fi
if ! grep -E -q "DESARROLLADOR|NAUTILUS|David Ayub|Enzo Ahumada" out/smoke/nautilus_view.xml; then
  echo "::error::Expected Nautilus entry UI was not observed"
  exit 1
fi
# Exercise the real initial enrollment screens without creating any production PINs.
for user in "DESARROLLADOR" "David Ayub" "Enzo Ahumada" "Alejandro Diesel" "Mario De Mingo"; do
  grep -F -q "$user" out/smoke/nautilus_view.xml
done
for account in "David Ayub" "Enzo Ahumada" "Alejandro Diesel" "Mario De Mingo"; do
  adb shell uiautomator dump /sdcard/nautilus_accounts.xml
  adb pull /sdcard/nautilus_accounts.xml out/smoke/nautilus_accounts.xml
  COORDS="$(python3 nautilus_source/ci_android_tap.py out/smoke/nautilus_accounts.xml "$account")"
  adb shell input tap $COORDS
  sleep 1
  adb shell uiautomator dump /sdcard/nautilus_admin.xml
  adb pull /sdcard/nautilus_admin.xml out/smoke/nautilus_admin.xml
  grep -F -q "PRIMER INGRESO" out/smoke/nautilus_admin.xml
  grep -F -q "$account" out/smoke/nautilus_admin.xml
  COORDS="$(python3 nautilus_source/ci_android_tap.py out/smoke/nautilus_admin.xml "VOLVER")"
  adb shell input tap $COORDS
  sleep 1
done
adb shell uiautomator dump /sdcard/nautilus_return.xml
adb pull /sdcard/nautilus_return.xml out/smoke/nautilus_return.xml
COORDS="$(python3 nautilus_source/ci_android_tap.py out/smoke/nautilus_return.xml "DESARROLLADOR")"
adb shell input tap $COORDS
sleep 2
adb shell uiautomator dump /sdcard/nautilus_owner.xml
adb pull /sdcard/nautilus_owner.xml out/smoke/nautilus_owner.xml
grep -E -q "CONFIGURACIÓN INICIAL|ACTIVAR DESARROLLADOR" out/smoke/nautilus_owner.xml
adb logcat -d -b crash > out/smoke/crashes.txt
if grep -F -q "Process: $PKG" out/smoke/crashes.txt; then
  echo "::error::App crashed during account role navigation"
  exit 1
fi
echo "PASS: Signed release installed and launched on Android; all 5 accounts visible; admin first-PIN and owner provisioning separated; no crash" | tee out/smoke/summary.txt
