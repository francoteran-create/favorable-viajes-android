#!/usr/bin/env python3
"""Make a self-contained technical handoff from a GitHub Actions verified Nautilus build.

Never packages signing keys, RSA owner PEM, or production records.
"""
from __future__ import annotations
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import zipfile

project = Path(os.environ["PROJECT"]).resolve()
assert (project / "settings.gradle").is_file(), f"Reconstructed Android project missing: {project}"
assert (project / "app/src/main").is_dir(), "Full source directory not found"
debug = project / "app/build/outputs/apk/debug/app-debug.apk"
assert debug.is_file() and debug.stat().st_size > 100_000, "Verified pilot APK not present"

output_dir = Path("out")
output_dir.mkdir(exist_ok=True)
handoff = output_dir / "NAUTILUS_MASTER_V115_TRASPASO"
if handoff.exists():
    shutil.rmtree(handoff)
handoff.mkdir()

repository = handoff / "01_REPOSITORIO_ORIGINAL"
repository.mkdir()
with tempfile.TemporaryDirectory() as td:
    archive = Path(td) / "git_head.tar"
    subprocess.run(["git", "archive", "--format=tar", "--output", str(archive), "HEAD"], check=True)
    with tarfile.open(archive, "r") as tf:
        for member in tf.getmembers():
            n = Path(member.name)
            assert not n.is_absolute() and ".." not in n.parts
        tf.extractall(repository, filter="data")

excludes = {".git", ".gradle", "build", ".idea", "local.properties"}
secret_extensions = {".pem", ".key", ".p12", ".jks", ".keystore"}
destination = handoff / "02_ANDROID_PROYECTO_COMPILABLE"

def ignore_secret_or_build(_dir: str, names: list[str]) -> set[str]:
    ignored = set()
    for name in names:
        lower = name.lower()
        if name in excludes or lower.endswith(tuple(secret_extensions)) or "private_key" in lower:
            ignored.add(name)
    return ignored

shutil.copytree(project, destination, ignore=ignore_secret_or_build)
assert (destination / "settings.gradle").is_file()
assert (destination / "app/src/main").is_dir()

pilots = handoff / "03_APK_PILOTO_NO_DISTRIBUIR"
pilots.mkdir()
shutil.copy2(debug, pilots / "Nautilus_Presentismo_V115_PILOTO.apk")
(pilots / "AVISO_FIRMA_TEMPORAL.txt").write_text(
    "APK PARA PRUEBAS SOLAMENTE. NO es la APK MASTER final. Puede usar firma temporal "
    "y NO garantiza actualizaciones sobre otra instalación. Hacer respaldo antes "
    "de cualquier reinstalación.\n", encoding="utf-8")

# Only include synthetic Android test evidence (never raw production attendance).
results = handoff / "04_RESULTADOS_PRUEBAS_SINTETICAS"
results.mkdir()
smoke = Path("out/smoke")
if smoke.is_dir():
    for file in smoke.iterdir():
        if file.is_file() and (
            file.name.endswith("_summary.txt")
            or file.name.endswith("_result.txt")
            or file.name in {"summary.txt", "process.txt", "start.txt", "NAUTILUS_MENSUAL_PILOTO.pdf"}
        ):
            shutil.copy2(file, results / file.name)

instructions = repository / "nautilus_source/LEEME_MASTER_TRASPASO_V115.md"
assert instructions.is_file()
shutil.copy2(instructions, handoff / "LEER_PRIMERO_INSTRUCCIONES.md")
(handoff / "INSTRUCCIONES_RAPIDAS.txt").write_text(
    "NAUTILUS COUNTRY - MASTER V115 PARA TERMINAR\n"
    "1) LEER_PRIMERO_INSTRUCCIONES.md: situación, pendientes y firma.\n"
    "2) 02_ANDROID_PROYECTO_COMPILABLE: abrir con Android Studio (Java 17/Gradle 8.2).\n"
    "3) 01_REPOSITORIO_ORIGINAL: fuente acumulada y GitHub Actions; no ejecutar transformaciones dos veces.\n"
    "4) 03_APK_PILOTO_NO_DISTRIBUIR: solo para pruebas.\n"
    "5) 04_RESULTADOS_PRUEBAS_SINTETICAS: evidencia de ensayos con empleados ficticios.\n"
    "6) Guardar claves privadas de licencias y keystore Android APARTE del paquete.\n"
    "7) Para la MASTER final: firma permanente + archivos reales del reloj + pruebas en teléfonos.\n",
    encoding="utf-8"
)

manifest = [
    "NAUTILUS MASTER V115 — PAQUETE TÉCNICO DE TRASPASO",
    f"GITHUB_SHA={os.environ.get('GITHUB_SHA', 'desconocido')}",
    f"GITHUB_RUN_ID={os.environ.get('GITHUB_RUN_ID', 'desconocido')}",
    "TIPO=MASTER DE CÓDIGO + PILOTO; NO ES RELEASE DEFINITIVO",
    "ARCHIVOS (bytes y SHA-256):",
]
for file in sorted(p for p in handoff.rglob("*") if p.is_file()):
    digest = hashlib.sha256(file.read_bytes()).hexdigest()
    manifest.append(f"{file.relative_to(handoff)} | {file.stat().st_size} | {digest}")
(handoff / "MANIFIESTO_MASTER.txt").write_text("\n".join(manifest) + "\n", encoding="utf-8")

out = output_dir / "NAUTILUS_MASTER_V115_CODIGO_APK_INSTRUCCIONES.zip"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for file in handoff.rglob("*"):
        if file.is_file():
            z.write(file, arcname=f"NAUTILUS_MASTER_V115_TRASPASO/{file.relative_to(handoff)}")
assert out.is_file() and out.stat().st_size > 200_000
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
print(f"MASTER HANDOFF OK: {out} ({out.stat().st_size:,} bytes), no private signing keys included")
