from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# Lightweight notification helper independent from the app's msg(title,detail,action).
mark=' void btn(String s,Runnable r){'
helper=''' void notice(String text){android.widget.Toast.makeText(this,text,android.widget.Toast.LENGTH_LONG).show();}\n'''
if 'void notice(String text)' not in s:s=s.replace(mark,helper+mark)
# Only convert one-argument msg calls introduced by V18/V19.
for prefix in ["Todavía no existe base para copiar","Backup creado: ","No se pudo crear backup: ","No se pudo abrir el backup","Backup restaurado","No se pudo restaurar: ","PDF generado: ","No se pudo generar PDF: "]:
    s=s.replace('msg("'+prefix,'notice("'+prefix)
# Fully qualify PDF drawing classes.
s=s.replace('Canvas c=page.getCanvas();Paint paint=new Paint(1);','android.graphics.Canvas c=page.getCanvas();android.graphics.Paint paint=new android.graphics.Paint(1);')
s=s.replace('V20 MASTER CANDIDATE','V21 VISUAL MASTER')
p.write_text(s)
print("V21 compile hardening applied")
