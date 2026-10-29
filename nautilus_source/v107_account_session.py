from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
old='''    securityUnlocked=false;
    securityOwner=false;
    securityPromptOpen=false;
    secLogin();'''
assert old in s
s=s.replace(old,'''    securityUnlocked=false;
    securityOwner=false;
    securityPromptOpen=false;
    secLogin();''',1)
# If app is resumed while a login dialog is active, do not open duplicate login dialogs.
needle='''void secLogin(){
  securityPromptOpen=true;'''
assert needle in s
# Preserve the explicit state of account switching and never re-use the prior account's unlocked flag.
needle='''mtAddLink("⇥","CAMBIAR DE USUARIO","Cerrar esta sesión y solicitar otro PIN",()->{'''
assert needle in s
# Do not allow a previously remembered bypass to skip credentials.
s=s.replace('if(secPrefs().getBoolean("skip_"+user,false)){','if(false&&secPrefs().getBoolean("skip_"+user,false)){',1)
p.write_text(s)
print("V107 disable remembered credential bypass for explicit account switching")
