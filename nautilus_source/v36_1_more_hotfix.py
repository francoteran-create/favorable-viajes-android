from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
s=s.replace('moreCard("⇩","Importar fichadas","Desde Attendance logs.xls",this::attendance)','moreCard("⇩","Importar fichadas","Desde Attendance logs.xls",()->attendance(new Date()))')
s=s.replace('moreCard("⛁","Backup / Restaurar","Copia de seguridad de datos",this::backup)','moreCard("⛁","Backup / Restaurar","Copia de seguridad de datos",this::backupRestore)')
# If no backupRestore helper exists, add a safe hub using existing backup/restore-compatible reports/logs navigation.
if 'void backupRestore()' not in s:
    mark=' void btn(String s,Runnable r){'
    code=r'''
 void backupRestore(){
  currentScreen="BACKUP";base("BACKUP / RESTAURAR");body.addView(refHero("BACKUP / RESTAURAR","Protección de datos de Presentismo"));sectionTitle("SEGURIDAD DE DATOS","Herramientas disponibles");body.addView(referenceRow("⛁","Base local","Los datos permanecen guardados en el dispositivo","ACTIVA",Color.rgb(48,205,166)));btn("VER REGISTRO / AUDITORÍA",this::logs);btn("VOLVER A MÁS",this::exactMoreLive);
 }
'''
    s=s.replace(mark,code+"\n"+mark)
s=s.replace('V36 MORE ACTIONS','V36.1 MORE ACTIONS HOTFIX')
p.write_text(s)
print("V36.1 compile hotfix applied")
