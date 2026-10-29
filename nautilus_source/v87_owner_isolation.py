from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# A fresh recipient install must be able to enroll a normal admin, NOT become owner.
s=s.replace('if(!secPrefs().contains("owner_hash")){secEnroll();return;}','if(!secPrefs().contains("owner_hash")){secLogin();return;}',1)
needle='''  if(!secPrefs().contains(user+"_hash")){
   new AlertDialog.Builder(this).setTitle("Cuenta sin activar")'''
assert needle in s
s=s.replace(needle,'''  if(index==0&&!secPrefs().contains(user+"_hash")){secEnroll();return;}
  if(index>0&&!secPrefs().contains(user+"_hash")){licFirstAdminPin(index);return;}
  if(!secPrefs().contains(user+"_hash")){
   new AlertDialog.Builder(this).setTitle("Cuenta sin activar")''',1)
code=r'''
 void licFirstAdminPin(int index){
  android.widget.EditText a=new android.widget.EditText(this),b=new android.widget.EditText(this);
  a.setHint("Crear PIN (4 a 6 números)");b.setHint("Repetir PIN");
  a.setInputType(18);b.setInputType(18);
  a.setFilters(new android.text.InputFilter[]{new android.text.InputFilter.LengthFilter(6)});
  b.setFilters(new android.text.InputFilter[]{new android.text.InputFilter.LengthFilter(6)});
  LinearLayout lay=new LinearLayout(this);lay.setOrientation(1);lay.addView(a);lay.addView(b);
  new AlertDialog.Builder(this).setTitle("PRIMER INGRESO · "+secNames[index-1])
   .setMessage("Elegí tu PIN local. La licencia dura tres meses desde el primer uso.")
   .setCancelable(false).setView(lay).setNegativeButton("VOLVER",(x,y)->secLogin())
   .setPositiveButton("CREAR",(x,y)->{
    String pin=a.getText().toString();
    if(!pin.matches("[0-9]{4,6}")||!pin.equals(b.getText().toString())){licFirstAdminPin(index);return;}
    secSet("admin_"+index,pin);
    securityPromptOpen=false;securityUnlocked=true;securityOwner=false;
    if(licActive())safeBootHome();else licExpired();
   }).show();
 }
'''
needle=' void licExpired(){'
assert needle in s
s=s.replace(needle,code+needle,1)
# No-owner-key devices must not use the permanent owner access to Nautilus.
needle='''  mtAddLink("▶","ENTRAR AL SISTEMA","Abrir Nautilus Presentismo",this::safeBootHome);'''
assert needle in s
s=s.replace(needle,'''  if(secPrefs().getBoolean("owner_issued",false))
   mtAddLink("▶","ENTRAR AL SISTEMA","Abrir Nautilus Presentismo",this::safeBootHome);''',1)
# Disable remembered bypass of the key ownership check.
s=s.replace('if(securityOwner)secAdminPanel();else safeBootHome();',
'''if(securityOwner)secAdminPanel();else if(licActive())safeBootHome();else licExpired();''')
p.write_text(s)
print("V87 separated first-run administrator setup from private-key-controlled owner")
