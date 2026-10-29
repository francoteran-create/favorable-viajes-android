# NAUTILUS COUNTRY — MASTER DE TRASPASO V115

**Rama fuente:** `nautilus-presentismo`  
**Repositorio:** `francoteran-create/favorable-viajes-android`  
**Estado:** MASTER técnica consolidada, **PILOTO** hasta cerrar pruebas en teléfono real y firma definitiva.  
**Regla:** no reiniciar el proyecto, no reemplazarlo por un mockup y no entregar como definitivo algo no verificado.

## 1. Qué contiene esta entrega

- `01_REPOSITORIO_ORIGINAL`: copia exacta del código de la rama, con historial técnico expresado por los scripts de evolución, pruebas y configuración de GitHub Actions.
- `02_ANDROID_PROYECTO_COMPILABLE`: proyecto Android **ya reconstruido con TODOS los transformadores acumulados hasta V115**. Abrir esta carpeta directamente en Android Studio. No hace falta volver a ejecutar las transformaciones sobre ella.
- `03_APK_PILOTO`: instalable **debug de prueba**. **Firma temporal: no distribuir como MASTER final ni prometer actualización sin reinstalación**.
- `04_RESULTADOS_DE_PRUEBAS`: evidencias del emulador y PDF sintético de control, cuando el flujo de GitHub haya generado esos archivos.
- `MANIFIESTO_MASTER.txt`: SHA del commit e identificadores/huellas SHA-256 de los archivos.
- Este documento: instrucciones para completar el desarrollo.

**IMPORTANTE:** el paquete deliberadamente NO incluye la clave privada de licencias del DESARROLLADOR, ninguna contraseña o certificado de firma privada. Esos materiales se custodian por separado.

## 2. Cómo abrir y continuar el desarrollo en Windows

1. Descomprimir todo el paquete en una carpeta local, por ejemplo `C:\\NAUTILUS_MASTER_V115\\`.
2. Instalar Android Studio y sus componentes de Android SDK. El proyecto de CI se compila con **Java 17 y Gradle 8.2**.
3. En Android Studio, elegir **Open** y abrir la carpeta `02_ANDROID_PROYECTO_COMPILABLE` (la que contiene `settings.gradle` o `settings.gradle.kts`).
4. Esperar la sincronización de Gradle y verificar el SDK instalado. Si aparece una ruta local de SDK faltante, configurar Android SDK desde el administrador de Android Studio.
5. Elegir **Build > Build APK(s)** o, desde una terminal en la raíz del proyecto y con Gradle 8.2 disponible, ejecutar `gradle :app:assembleDebug`.
6. Para generar un release **sin firma**: `gradle :app:assembleRelease`. Un release sin firmar no se instala ni debe distribuirse.
7. **No ejecutar de nuevo** `nautilus_source/v9_management.py` sobre el proyecto reconstruido: sus transformadores no son una migración repetible sobre la salida final. Para reproducir desde cero usar la CI del repositorio original.

## 3. Lo que ya se probó

En GitHub Actions sobre Android 10 (API 29), con datos **ficticios** de prueba:

- Firma criptográfica de licencias, rechazo de firma falsa, código alterado y fecha incorrecta: 18 pruebas.
- Lector XML Spreadsheet 2003 de personal, duplicados, codificación y archivos inválidos: 15 pruebas.
- Lector de marcaciones, fechas, celdas vacías y archivos inválidos: 18 pruebas.
- Construcción de APK debug y release ofuscada; firma **descartable** para pruebas de release.
- Inicio con selección de cinco perfiles: DESARROLLADOR, David Ayub, Enzo Ahumada, Alejandro Diesel y Mario De Mingo.
- Crear PIN real de prueba para David, ingresar, cambiar de usuario y comprobar que no ve el panel exclusivo.
- Seleccionar **Attendance Report.xls** y **Attendance logs.xls** desde Android e importar 2 empleados y 4 fichadas sintéticos.
- Generar el PDF mensual, guardarlo desde el cuadro de diálogo Android y verificar que es un PDF completo.
- El PDF de muestra V115 muestra resumen por empleado y total general en formato A4.

Las pruebas automáticas **no reemplazan** la validación de los cálculos con los dos archivos reales del reloj ni el uso cotidiano en un teléfono físico.

## 4. Pendientes obligatorios para la MASTER definitiva

### A — Verificación funcional con el consorcio
- Importar originales **Attendance Report.xls** (ID, nombre, departamento) y **Attendance logs.xls** (ID, nombre, fecha/hora); comparar la cantidad de empleados y marcaciones con el reloj. La extensión `.xls` no garantiza el formato: el importador integrado espera **Excel XML Spreadsheet 2003**, no BIFF binario ni XLSX comprimido. Si el reloj entrega otro formato, añadir soporte real y pruebas, sin renombrar archivos para simular compatibilidad.
- Comparar manualmente una muestra de turnos 5x2, 4x2, 6x1, francos, nocturnos, entrada/salida incompleta, retrasos, recargos, cambios de mes y días sin fichadas.
- Validar fechas y totales del PDF mensual con esos datos, revisar su presentación en Android y compartirlo.
- Confirmar permisos de los cuatro administradores y el retorno exclusivo al panel DESARROLLADOR.
- Probar generación y renovación de licencia **desde la interfaz** con el PEM privado del propietario, emisión del código, activación en otro teléfono, reutilización de código y vencimiento real/fecha alterada. No asumir que 18 pruebas unitarias cubren todo el flujo UI.
- Hacer copia de seguridad y una prueba de recuperación; nunca perder datos de producción por reinstalar.

### B — Firma permanente de APK
- Hay dos secretos **diferentes**. `NAUTILUS_CLAVE_DESARROLLADOR_PRIVADA.pem` es para **firmar códigos de licencia** (RSA) y NO sirve para firmar la APK. La clave de firma Android es un archivo de certificado/keystore separado.
- El propietario tiene el **kit privado de firma MASTER**, entregado por separado. Su archivo `github_release_bundle.txt` sirve para crear el secreto de GitHub Actions llamado exactamente **`NAUTILUS_RELEASE_SIGNING_BUNDLE`**.
- En GitHub: repositorio > **Settings > Secrets and variables > Actions > New repository secret**. Crear el secreto `NAUTILUS_RELEASE_SIGNING_BUNDLE` y pegar el texto del `github_release_bundle.txt`. NUNCA copiarlo al código, al ZIP compartido, ni a una conversación pública.
- Ejecutar `.github/workflows/nautilus-build.yml` sobre `nautilus-presentismo`. Si el secreto es válido, la acción generará el artefacto **`NAUTILUS-MASTER-RELEASE-FIRMADA`**. Verificar firma, paquete, versionCode y compatibilidad de actualización.
- **No usar** para distribución la APK debug incluida en este ZIP ni la release firmada con certificado descartable de CI.
- Antes de actualizar una instalación existente, comparar certificados. Si son diferentes Android rechazará la actualización; NO desinstalar si contiene datos sin respaldar.

### C — Cierre y entrega
- Instalar el release permanente en dos teléfonos distintos sin datos reales para probar licencias y permisos.
- Realizar una actualización sobre esa misma firma **sin perder datos**.
- Validar la importación de ambos Excel originales, cálculos de jornadas y guardado de PDF A4.
- Realizar la aceptación del propietario y registrar versión, SHA-256, fecha, firma y archivo firmado.
- Recién entonces marcar como **MASTER DEFINITIVA**.

## 5. Cómo iniciar otra sesión de desarrollo sin perder el trabajo

Compartir **este ZIP MASTER técnico**, no solamente el APK de prueba. Abrir `02_ANDROID_PROYECTO_COMPILABLE` como código de referencia y `01_REPOSITORIO_ORIGINAL` como trazabilidad. Trabajar únicamente sobre la rama `nautilus-presentismo` y conservar todo lo que ya funciona.

### Instrucción lista para copiar a otro desarrollador o chat

> Continuá Nautilus Presentismo desde esta MASTER V115 exacta. NO rehagas la app, NO conviertas nada en maqueta. El código completo está en `02_ANDROID_PROYECTO_COMPILABLE`, y el historial acumulado en `01_REPOSITORIO_ORIGINAL`. Primero verificá las pruebas de CI de 18 licencias, 15 importación de personal, 18 importación de fichadas y Android 10 (dos empleados + cuatro marcas + PDF guardado). Tu misión es cerrar, con pruebas reales, los tres pendientes: a) originales del reloj y exactitud de jornadas, b) circuito completo de licencias en dispositivos, c) release firmado permanentemente que actualice sin pérdida de datos. Conservá diseño y funcionalidad. Hacé avances grandes, un único ZIP completo al entregar, con código, APK firmada, pruebas y changelog. Nunca simules verificaciones.

## 6. Advertencias importantes

- **No introducir PIN reales, archivos de personal ni claves privadas en el repositorio GitHub.**
- El PIN `123456` de los ensayos es **únicamente para el emulador**: no es un PIN predeterminado de producción.
- Una licencia que funciona sin servidor puede tener limitaciones frente a reinstalación o borrado de datos. No prometer activación única global infalible sin backend.
- El informe presenta horas y recargos **orientativos, no liquidación salarial aprobada**.
- No confundir un porcentaje de avance estimado con una validación final: el cierre se prueba, no se presume.

**Resumen:** el proyecto está muy adelantado, pero para distribuirlo como producto definitivo faltan firma permanente, datos reales y pruebas físicas de licencias/actualización.
