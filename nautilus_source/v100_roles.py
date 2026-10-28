from pathlib import Path
import os
j=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=j.read_text()
s=s.replace('base("SUPERADMIN · USUARIOS");','base("DESARROLLADOR · CONTROL GENERAL");',1)
s=s.replace('setTitle("NAUTILUS · INGRESAR")','setTitle("NAUTILUS · ACCESO PERSONAL")',1)
j.write_text(s)
print("V100 roles shown clearly")