from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
marker='''currentScreen="CONFIG";mtScreen("CONFIGURACIÓN",4);'''
assert marker in s,"Configuration screen entry changed"
extra=r'''
  // Access is available from the fixed CONFIG. tab and header menu, not hidden below the home scroll.
  if(securityUnlocked){
   if(securityOwner&&licDeveloperAuthorized()){
    mtAddLink("⚙","VOLVER AL PANEL DESARROLLADOR",
      "Administración exclusiva y generación de licencias",this::secAdminPanel);
   }
   mtAddLink("⇥","CAMBIAR DE USUARIO","Cerrar sesión y solicitar otro PIN",()->{
    securityUnlocked=false;
    securityOwner=false;
    securityPromptOpen=false;
    secLogin();
   });
  }
'''
assert 'VOLVER AL PANEL DESARROLLADOR' in s,"Existing owner entry expected"
s=s.replace(marker,marker+extra,1)
p.write_text(s)
print("V112: fixed navigation CONFIGURATION screen now exposes safe user switching and authorized owner panel")
