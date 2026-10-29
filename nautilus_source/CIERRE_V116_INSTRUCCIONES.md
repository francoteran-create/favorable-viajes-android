# NAUTILUS PRESENTISMO — CIERRE V116 (29-10-2026)

Rama: `nautilus-presentismo`. No mezclar con FAVORABLE VIAJES en `main`.

## Cambio funcional incorporado
En el diagrama individual del empleado, mostrar en tarjetas con texto multilínea:
- día y régimen;
- **ENTRADA PROGRAMADA** y **SALIDA PROGRAMADA**;
- **PRIMERA FICHADA** y **ÚLTIMA FICHADA**, cuando existan;
- **UNA FICHADA: REVISAR** (sin inventar salida);
- **SIN FICHADAS IMPORTADAS** y **FRANCO** identificados.

El detalle diario sigue siendo editable por toque. Los campos de fichada muestran el primer y último registro del mismo día calendario. **Advertencia importante:** en turnos nocturnos con salida al día siguiente, no se debe interpretar esa vista como apareamiento definitivo de entrada y salida: comprobar la jornada nocturna con el informe detallado antes de usar datos para liquidación.

## Resultado comprobado
- La ejecución de GitHub Actions número 409, run 40888360779, terminó con conclusión `success`.
- Artefacto generado: `NAUTILUS-PRESENTISMO-V9-MASTER-APK` (nombre heredado del flujo).
- La ejecución observada no certifica por sí sola la presentación visual en un teléfono físico ni la firma permanente.
- La V115 anterior contiene las instrucciones y scripts acumulados de empaquetado y validación ampliada.

## Checklist indispensable para dar por terminada la MASTER
1. Guardar respaldo de datos de la instalación existente.
2. Verificar que el certificado de firma del APK nuevo sea compatible con el instalado antes de intentar actualizar. Si no coincide, **no desinstalar**.
3. Revisar un diagrama 5x2, 4x2, 6x1 y un FRANCO; confirmar que los textos completos entran en pantalla.
4. Importar una muestra real del reloj y controlar 0, 1 y 2 fichadas, duplicados y turno nocturno.
5. Revisar roles: cuatro administradores, panel exclusivo de DESARROLLADOR, PIN y licencia.
6. Exportar y guardar PDF mensual; verificarlo manualmente si se necesita como documento.
7. Generar release con keystore permanente, instalar en dos teléfonos y comprobar una actualización sin pérdida de datos.
8. Publicar el paquete fuente y APK firmado **solo cuando** todos los puntos estén aprobados.

No subir a GitHub: claves privadas, PIN reales, datos del personal, ni el archivo de secretos del propietario.
