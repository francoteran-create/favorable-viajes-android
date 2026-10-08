from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
marker=" void sectorStats(){"
assert marker in s
code=r"""
 void managementSummary(){
  base("CONTROL DE PERSONAL");
  body.addView(muted("Indicadores para gestión · mes actual"));
  btn("ESTADÍSTICAS POR TRABAJADOR",this::workerStats);
  btn("ESTADÍSTICAS POR SECTOR",this::sectorStats);
  btn("RANKING DEL PERSONAL",this::workerRanking);
  btn("INCIDENCIAS PENDIENTES",this::reviews);
  btn("RESUMEN PARA LIQUIDACIÓN",this::payrollSummary);
  btn("CIERRE MENSUAL",this::monthClose);
 }
"""
s=s.replace(marker,code+"\n"+marker)
s=s.replace('void statsHub(){','void statsHub(){')
s=s.replace('btn("ESTADÍSTICAS · PERSONAL Y SECTORES",this::statsHub);','btn("CONTROL Y ESTADÍSTICAS",this::managementSummary);')
p.write_text(s)
