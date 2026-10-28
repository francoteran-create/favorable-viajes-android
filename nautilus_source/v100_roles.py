from pathlib import Path
import os
j=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=j.read_text()
assert 'base("SUPERADMIN · USUARIOS");' in s
s=s.replace('base("SUPERADMIN · USUARIOS");','base("DESARROLLADOR · CONTROL GENERAL");',1)
assert 'setTitle("NAUTILUS · INGRESAR")' in s
s=s.replace('setTitle("NAUTILUS · INGRESAR")','setTitle("NAUTILUS · ACCESO PERSONAL")',1)
j.write_text(s)
print("V100 roles shown clearly")