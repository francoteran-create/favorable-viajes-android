from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void dualClockHub(){'
assert mark in s
code=r'''
 boolean securityUnlocked=false, securityOwner=false, securityPromptOpen=false;
 android.content.SharedPreferences secPrefs(){return getSharedPreferences("nautilus_auth_v83",MODE_PRIVATE);}
 String secSalt(){byte[] b=new byte[16];new java.security.SecureRandom().nextBytes(b);return android.util.Base64.encodeToString(b,2);}
 String secHash(String pass,String salt){
  try{byte[] b=javax.crypto.SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256").generateSecret(
   new javax.crypto.spec.PBEKeySpec(pass.toCharArray(),android.util.Base64.decode(salt,2),180000,256)).getEncoded();
   return android.util.Base64.encodeToString(b,2);
  }catch(Exception ex){throw new RuntimeException(ex);}
 }
 void secSet(String user,String pass){
  String salt=secSalt();if(!secPrefs().edit().putString(user+"_salt",salt).putString(user+"_hash",secHash(pass,salt)).commit())throw new RuntimeException("No se pudo guardar la contraseña");
 }
 boolean secCheck(String user,String pass){
  String salt=secPrefs().getString(user+"_salt",""),hash=secPrefs().getString(user+"_hash","");
  if(salt.isEmpty()||hash.isEmpty())return false;
  return java.security.MessageDigest.isEqual(hash.getBytes(java.nio.charset.StandardCharsets.UTF_8),
    secHash(pass,salt).getBytes(java.nio.charset.StandardCharsets.UTF_8));
 }
 String[] secNames={"David Ayub","Enzo Ahumada","Alejandro Diesel","Mario De Mingo"};
 void secGate(){
  if(securityUnlocked||securityPromptOpen)return;
  securityPromptOpen=true;
  securityOwner=false;
  if(!secPrefs().contains("owner_hash")){secEnroll();return;}
  secLogin();
 }
 void secEnroll(){
  securityPromptOpen=true;
  android.widget.EditText a=new android.widget.EditText(this),b=new android.widget.EditText(this);
  a.setHint("PIN nuevo (4 a 6 números)");b.setHint("Repetir PIN");
  a.setInputType(18);b.setInputType(18);a.setFilters(new android.text.InputFilter[]{new android.text.InputFilter.LengthFilter(6)});b.setFilters(new android.text.InputFilter[]{new android.text.InputFilter.LengthFilter(6)});
  LinearLayout lay=new LinearLayout(this);lay.setOrientation(1);lay.setPadding(20,12,20,12);lay.addView(a);lay.addView(b);
  new AlertDialog.Builder(this).setTitle("CREAR SUPERADMINISTRADOR")
   .setMessage("Primer acceso local. Esta cuenta no vence. Guardá tu contraseña.")
   .setView(lay).setCancelable(false).setPositiveButton("ACTIVAR",(d,w)->{
    String pass=a.getText().toString();
    if(!pass.matches("[0-9]{4,6}")||!pass.equals(b.getText().toString())){securityPromptOpen=false;new AlertDialog.Builder(this).setMessage("El PIN debe tener entre 4 y 6 números y coincidir.").setPositiveButton("REINTENTAR",(x,y)->secGate()).show();return;}
    secSet("owner",pass);securityUnlocked=true;securityOwner=true;securityPromptOpen=false;secPrefs().edit().putBoolean("owner_pin",true).apply();secAdminPanel();
   }).show();
 }
 void secLogin(){
  securityPromptOpen=true;
  String[] names=new String[5];names[0]="SUPERADMINISTRADOR";
  for(int i=0;i<4;i++)names[i+1]=secNames[i];
  new AlertDialog.Builder(this).setTitle("NAUTILUS · INGRESAR")
   .setCancelable(false).setItems(names,(d,index)->secPassword(index)).show();
 }
 void secPassword(int index){
  securityPromptOpen=true;
  String user=index==0?"owner":"admin_"+index;
  if(!secPrefs().contains(user+"_hash")){
   new AlertDialog.Builder(this).setTitle("Cuenta sin activar")
    .setMessage("El superadministrador debe asignar la contraseña de esta cuenta.")
    .setPositiveButton("VOLVER",(d,w)->secLogin()).setCancelable(false).show();return;
  }
  if(secPrefs().getBoolean("skip_"+user,false)){securityUnlocked=true;securityOwner=index==0;securityPromptOpen=false;if(index==0&&!secPrefs().getBoolean("owner_pin",false))secOwnerPin();else if(securityOwner)secAdminPanel();else safeBootHome();return;}
  android.widget.EditText input=new android.widget.EditText(this);input.setHint("PIN numérico");input.setInputType(18);
  if(index==0&&!secPrefs().getBoolean("owner_pin",false)){input.setHint("Contraseña anterior, una sola vez");input.setInputType(129);}else input.setFilters(new android.text.InputFilter[]{new android.text.InputFilter.LengthFilter(6)});
  new AlertDialog.Builder(this).setTitle(index==0?"SUPERADMINISTRADOR":secNames[index-1])
   .setView(input).setCancelable(false).setNegativeButton("VOLVER",(d,w)->secLogin())
   .setPositiveButton("INGRESAR",(d,w)->{
    if(secCheck(user,input.getText().toString())){
     securityUnlocked=true;securityOwner=index==0;securityPromptOpen=false;if(securityOwner)secAdminPanel();else safeBootHome();
    }else{
     new AlertDialog.Builder(this).setTitle("Contraseña incorrecta")
      .setPositiveButton("REINTENTAR",(x,y)->secPassword(index)).setCancelable(false).show();
    }
   }).show();
 }
 void secOwnerPin(){
  android.widget.EditText first=new android.widget.EditText(this),again=new android.widget.EditText(this);
  first.setHint("Nuevo PIN (4 a 6 dígitos)");again.setHint("Repetir PIN");
  first.setInputType(18);again.setInputType(18);
  first.setFilters(new android.text.InputFilter[]{new android.text.InputFilter.LengthFilter(6)});
  again.setFilters(new android.text.InputFilter[]{new android.text.InputFilter.LengthFilter(6)});
  LinearLayout panel=new LinearLayout(this);panel.setOrientation(1);panel.addView(first);panel.addView(again);
  new AlertDialog.Builder(this).setTitle("CONFIGURAR PIN NUMÉRICO").setCancelable(false).setView(panel)
   .setPositiveButton("GUARDAR",(d,w)->{
    String pin=first.getText().toString();
    if(!pin.matches("[0-9]{4,6}")||!pin.equals(again.getText().toString())){secOwnerPin();return;}
    secSet("owner",pin);secPrefs().edit().putBoolean("owner_pin",true).commit();secAdminPanel();
   }).show();
 }
 void secAdminPanel(){
  if(!securityOwner||!securityUnlocked){secGate();return;}
  base("SUPERADMIN · USUARIOS");
  for(int i=0;i<4;i++){
   final int n=i+1;
   mtAddLink("♙",secNames[i],secPrefs().contains("admin_"+n+"_hash")?"CAMBIAR CONTRASEÑA":"ACTIVAR ADMINISTRADOR",()->secSetAdmin(n));
  }
  mtAddLink("♧",secPrefs().getBoolean("skip_owner",false)?"DESACTIVAR ENTRADA DIRECTA":"ENTRAR SIN CONTRASEÑA","Recordar esta decisión en este teléfono",()->{boolean old=secPrefs().getBoolean("skip_owner",false);secPrefs().edit().putBoolean("skip_owner",!old).apply();secAdminPanel();});
  mtAddLink("▶","ENTRAR AL SISTEMA","Abrir Nautilus Presentismo",this::safeBootHome);
  mtAddLink("⇥","CERRAR SESIÓN","Bloquear el acceso",()->{securityUnlocked=false;securityPromptOpen=false;secGate();});
 }
 void secSetAdmin(int index){
  if(!securityOwner||!securityUnlocked){secGate();return;}
  android.widget.EditText input=new android.widget.EditText(this);input.setInputType(129);
  input.setHint("PIN de 4 a 6 números");input.setInputType(18);input.setFilters(new android.text.InputFilter[]{new android.text.InputFilter.LengthFilter(6)});
  new AlertDialog.Builder(this).setTitle(secNames[index-1]).setView(input)
   .setNegativeButton("CANCELAR",null).setPositiveButton("GUARDAR",(d,w)->{
    String pass=input.getText().toString();
    if(pass.matches("[0-9]{4,6}"))secSet("admin_"+index,pass);
    secAdminPanel();
   }).show();
 }
'''
s=s.replace(mark,code+'\n'+mark,1)
# The Android activity resumes after its original initialization. Invoke the
# non-cancelable gate from onResume, without tampering with its existing boot.
# v83 is an access prototype only; distributed licensing is NOT yet enabled.
mark=' void dualClockHub(){'
assert mark in s
s=s.replace(mark,''' @Override protected void onResume(){super.onResume();if(!securityUnlocked)secGate();}
'''+mark,1)
# Owner controls are reachable from the owner login landing screen.
p.write_text(s)
print("Local login module applied")
