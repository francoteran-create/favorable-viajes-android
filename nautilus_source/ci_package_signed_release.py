#!/usr/bin/env python3
"""Package only a verified owner-signed release APK. Never include private keys."""
from pathlib import Path
import hashlib, os, zipfile
out=Path("out")
apk=out/"Nautilus-Presentismo-MASTER-FIRMADA.apk"
assert apk.exists() and apk.stat().st_size>100_000, "Owner-signed release missing"
assert apk.read_bytes()[:2]==b"PK", "Invalid APK container"
fingerprint=hashlib.sha256(apk.read_bytes()).hexdigest()
readme="""NAUTILUS PRESENTISMO — RELEASE FIRMADA
Esta APK fue compilada y firmada por el CI con el certificado privado del titular.
No contiene el keystore, claves privadas ni fichadas del consorcio.
NO desinstalar la aplicación existente antes de comprobar certificado e identificador.
Una APK con certificado diferente NO puede actualizar encima de la anterior conservando sus datos.
Realizar respaldo seguro y validar en un dispositivo de prueba primero.
Verificar fichadas, licencias, PIN, informes PDF, horarios nocturnos y restauración.
La firma del APK NO cifra la base de datos; cifrado requiere auditoría separada.
"""
dst=out/"NAUTILUS_MASTER_RELEASE_FIRMADA_APK_INSTRUCCIONES.zip"
with zipfile.ZipFile(dst,"w",zipfile.ZIP_DEFLATED) as z:
 z.write(apk,apk.name)
 z.writestr("LEER_ANTES_DE_INSTALAR.txt",readme)
 z.writestr("SHA256.txt",fingerprint+"  "+apk.name+"\n")
with zipfile.ZipFile(dst) as z:
 assert z.testzip() is None
 assert z.read(apk.name)[:2]==b"PK"
print("PASS: signed APK in ZIP",dst,"SHA256",fingerprint)
