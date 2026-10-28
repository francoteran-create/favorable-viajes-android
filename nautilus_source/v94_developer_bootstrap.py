from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
old='''if(index==0&&!secPrefs().contains(user+"_hash")){
   new AlertDialog.Builder(this).setTitle("DESARROLLADOR")
    .setMessage("Este teléfono no está configurado como dispositivo del desarrollador.")
    .setCancelable(false).setPositiveButton("VOLVER",(x,y)->secLogin()).show();return;
  }'''
assert old in s
new='''if(index==0&&!secPrefs().contains(user+"_hash")){
   new AlertDialog.Builder(this).setTitle("ACTIVAR DESARROLLADOR")
    .setMessage("Solo podés habilitar esta cuenta con tu clave privada original de Nautilus. Los administradores no necesitan este paso.")
    .setCancelable(false)
    .setNegativeButton("VOLVER",(x,y)->secLogin())
    .setPositiveButton("AUTORIZAR ESTE TELÉFONO",(x,y)->{
      securityOwner=true;securityUnlocked=true;securityPromptOpen=true;
      licImportOwnerKey();
    }).show();return;
  }'''
s=s.replace(old,new,1)
old='''.setPositiveButton("CONTINUAR",(x,y)->secAdminPanel()).show();'''
assert old in s
s=s.replace(old,'''.setPositiveButton("CONTINUAR",(x,y)->{
      if(!secPrefs().contains("owner_hash"))secEnroll();
      else secAdminPanel();
    }).show();''',1)
# PIN enrollment only after successful proof-of-possession.
old='''void secEnroll(){
  securityPromptOpen=true;'''
assert old in s
s=s.replace(old,'''void secEnroll(){
  if(!licDeveloperAuthorized()){securityUnlocked=false;securityPromptOpen=false;secGate();return;}
  securityPromptOpen=true;''',1)
p.write_text(s)
print("V94 safe first-time developer enrollment after private key verification")
