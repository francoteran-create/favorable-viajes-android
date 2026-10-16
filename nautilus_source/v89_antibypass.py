from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# Refuse unauthorized owner access even if somebody recreates an owner PIN.
needle='''  if(!securityOwner||!securityUnlocked){secGate();return;}
  base("PANEL DEL DESARROLLADOR");'''
assert needle in s, "Developer access entrypoint changed"
s=s.replace(needle,'''  if(!securityOwner||!securityUnlocked){secGate();return;}
  // The developer PIN alone is insufficient to obtain permanent privileges.
  if(!secPrefs().getBoolean("owner_issued",false)){
   base("DESARROLLADOR · ACTIVACIÓN");
   mtAddLink("♧","HABILITAR GENERADOR","Acreditar clave privada exclusiva",this::licImportOwnerKey);
   mtAddLink("⇥","VOLVER","Selección de usuario",()->{securityUnlocked=false;securityPromptOpen=false;secGate();});
   return;
  }
  base("PANEL DEL DESARROLLADOR");''',1)
# Verify owner authorization before presenting the main system.
needle='''  if(secPrefs().getBoolean("owner_issued",false))
   mtAddLink("▶","ENTRAR AL SISTEMA","Abrir Nautilus Presentismo",this::safeBootHome);'''
assert needle in s
# Existing saved login bypasses are reviewed at runtime, not only the login selector.
needle=''' @Override protected void onResume(){super.onResume();if(!securityUnlocked)secGate();}'''
assert needle in s
s=s.replace(needle,''' @Override protected void onResume(){
  super.onResume();
  if(!securityUnlocked){secGate();return;}
  if(!securityOwner&&!licActive()&&!securityPromptOpen){
   securityPromptOpen=true;
   licExpired();
  }
 }''',1)
# Do not leave unlocked session active after a bad expired-key attempt.
needle='''if(licAccept(code.getText().toString())){securityUnlocked=true;safeBootHome();}'''
assert needle in s
s=s.replace(needle,'''if(licAccept(code.getText().toString())){securityPromptOpen=false;securityUnlocked=true;safeBootHome();}''',1)
p.write_text(s)
print("V89 guards developer privilege and checks active license on Android resume")
