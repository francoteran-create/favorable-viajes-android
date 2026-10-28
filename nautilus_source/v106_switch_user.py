from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
needle='''   mtAddLink("⚙","VOLVER AL PANEL DESARROLLADOR","Administrar usuarios y generar licencias",this::secAdminPanel);
  }'''
assert needle in s
s=s.replace(needle,'''   mtAddLink("⚙","VOLVER AL PANEL DESARROLLADOR","Administrar usuarios y generar licencias",this::secAdminPanel);
  }
  if(securityUnlocked){
   mtAddLink("⇥","CAMBIAR DE USUARIO","Cerrar esta sesión y solicitar otro PIN",()->{
    securityUnlocked=false;
    securityOwner=false;
    securityPromptOpen=false;
    secLogin();
   });
  }''',1)
p.write_text(s)
print("V106 secure change-user shortcut on home for all accounts")
