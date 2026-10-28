from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
anchor='''  mtAddLink("▶","ENTRAR AL SISTEMA"'''
assert anchor in s
new='''  mtAddLink("▣","ESTADO DE LICENCIAS","Verificar fecha, vigencia y generador",()->{
   if(!securityOwner||!securityUnlocked||!licDeveloperAuthorized()){securityUnlocked=false;securityOwner=false;securityPromptOpen=false;secGate();return;}
   new AlertDialog.Builder(this).setTitle("CONTROL DE LICENCIAS")
    .setMessage(licStatus()+"\\nGenerador: AUTORIZADO\\nCódigos: válidos solo en la fecha de emisión\\nRenovación: tres meses desde la activación")
    .setPositiveButton("VOLVER",(d,w)->secAdminPanel()).show();
  });
'''
s=s.replace(anchor,new+anchor,1)
p.write_text(s)
print("V102 developer-only license diagnostics")
