from pathlib import Path
import os
j=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=j.read_text()
old='''.setMessage("Solo podés habilitar esta cuenta con tu clave privada original de Nautilus. Los administradores no necesitan este paso.")'''
assert old in s
s=s.replace(old,'''.setMessage("Configuración exclusiva, por única vez. Después ingresarás con tu PIN personal sin volver a elegir archivos. La clave de firma no se comparte con los administradores.")''',1)
# Avoid privileged state lingering during cancelled first-time file selection.
old='''      securityOwner=true;securityUnlocked=true;securityPromptOpen=true;
      licImportOwnerKey();'''
assert old in s
s=s.replace(old,'''      securityOwner=true;securityUnlocked=true;securityPromptOpen=true;
      licImportOwnerKey();''',1)
# State clearly which authentication phase this is.
s=s.replace('setTitle("ACTIVAR DESARROLLADOR")','setTitle("CONFIGURACIÓN INICIAL · DESARROLLADOR")',1)
j.write_text(s)
print("V101 single provisioning explanation, then personal PIN")
