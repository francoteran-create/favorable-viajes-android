from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# Ensure photo picker result actually saves; earlier transformer skipped hook in some generated sources.
sig='protected void onActivityResult(int requestCode,int resultCode,Intent data){'
if sig in s and 'requestCode==902&&resultCode==RESULT_OK' not in s:
 s=s.replace(sig,sig+'if(requestCode==902&&resultCode==RESULT_OK&&data!=null&&data.getData()!=null){saveEmployeePhoto(data.getData());return;}',1)
# Make PERSONAL lead to the actual personnel management list, with an explicit create/configuration entry.
i=s.find('void employees()')
if i>=0:
 j=s.find('{',i)+1
 if 'CARGAR / CONFIGURAR PERSONAL' not in s[i:s.find('\n }',i)]:
  s=s[:j]+'\n  btn("CARGAR / CONFIGURAR PERSONAL",this::pending);\n'+s[j:]
# Every personnel profile gets a direct master-file editor and photo access.
i=s.find('void exactPersonal(')
if i>=0:
 end=s.find('\n }',i)
 blk=s[i:end]
 if 'EDITAR FICHA Y FOTO' not in blk:
  pos=blk.find(';',blk.find('base('))+1
  blk=blk[:pos]+'btn("EDITAR FICHA Y FOTO",()->personnelMasterForm(pid));'+blk[pos:]
  s=s[:i]+blk+s[end:]
# Bottom nav in MASTER must always return to MASTER itself, not legacy screens.
s=s.replace('bottomTab("⌂","INICIO",this::referenceHome)','bottomTab("⌂","INICIO",this::masterImageHome)')
s=s.replace('bottomTab("⌂","INICIO",this::exactToday)','bottomTab("⌂","INICIO",this::masterImageHome)')
# Android Back from main module screens should have an obvious on-screen HOME path too.
s=s.replace('base("FICHA DEL PERSONAL");','base("FICHA DEL PERSONAL");btn("⌂ INICIO",this::masterImageHome);',1)
s=s.replace("V53 MASTER COMPONENTS ONLY","V54 PERSONNEL PHOTO + HOME NAV")
p.write_text(s);print("V54: personnel master/photo exposed; home route reinforced")
