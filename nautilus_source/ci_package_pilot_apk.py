#!/usr/bin/env python3
"""Create a tested pilot handoff ZIP from the APK built by GitHub Actions.
No personal attendance data or signing credentials are packed.
"""
from pathlib import Path
import os, zipfile, hashlib

project=Path(os.environ["PROJECT"])
apk=project/"app/build/outputs/apk/debug/app-debug.apk"
if not apk.is_file() or apk.stat().st_size < 100000:
    raise SystemExit("Android APK missing: pilot package will not be published")
out=Path("out")
out.mkdir(exist_ok=True)
target=out/"NAUTILUS_PRESENTISMO_V116_3_PILOTO_APK_INSTRUCCIONES.zip"
sha=hashlib.sha256(apk.read_bytes()).hexdigest()
readme=f"""NAUTILUS PRESENTISMO V116.3 — PILOTO ANDROID
Rama: nautilus-presentismo
Commit: {os.environ.get('GITHUB_SHA','sin identificar')}
APK SHA256: {sha}
Archivo: Nautilus-Presentismo-V116.3-PILOTO.apk

Esta APK es de pruebas. Su certificado de firma puede ser temporal.
NO desinstalar la aplicación anterior sin respaldar los datos.
Si Android rechaza actualizar, conservar la versión anterior.
Probar primero en un teléfono sin datos de producción.

VALIDACIONES PENDIENTES PARA CIERRE DEFINITIVO
- Importar los XLS reales del reloj y comparar fichadas por empleado.
- Verificar jornadas nocturnas que atraviesan medianoche.
- Confirmar el acceso de cuatro administradores y el panel DESARROLLADOR.
- Validar claves de licencia y firma permanente del instalable.
- Confirmar actualización en el dispositivo sin perder datos.

El ZIP NO incluye claves privadas ni datos de personal.
"""
with zipfile.ZipFile(target,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    z.write(apk,"Nautilus-Presentismo-V116.3-PILOTO.apk")
    z.writestr("LEER_PRIMERO.txt",readme)
with zipfile.ZipFile(target) as z:
    assert z.testzip() is None
    assert z.read("Nautilus-Presentismo-V116.3-PILOTO.apk")[:2] == b"PK"
print(f"ZIP OK: {target} bytes={target.stat().st_size} APK_SHA256={sha}")
