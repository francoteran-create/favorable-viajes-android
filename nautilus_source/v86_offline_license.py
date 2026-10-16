from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void dualClockHub(){'
assert mark in s
code=r'''
 // V86: Offline licensing. Private signing key is not shipped in distributed APK.
 static final String LICENSE_PUBLIC_KEY="MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnna3me1dUgKR8HtVBDxeocqLMvhzX5qQvPBJHffPdSsdcFSj4H1xvwR/t/17gFhQwjTfKcy0Mk9ubEJJ5fApfTlXyGdwOL7Hh3SrZ3SlJj0r69rZHKlPszb4MZ9I87aMFVnn4RxSjdXDJDTqYeA68YVYEB2AdyylcoDXiKVMEG+px9HCmdtI/875mRb0T07vPtHRsLBbI5eD+AxIZ3TmN0avhLKWqvK1tjzjj6WXY1gm00bktMjU0xPu+VckBya/buJonDieVbtIV4ABH2k76QhGoqcmXrRDA4XEfREjGHfrWVcYVLYzOPMEeQKa/xjNpdEAR3QbmZyk2Mk5SQd2NQIDAQAB";
 java.security.PublicKey licPublicKey()throws Exception{
  byte[] data=android.util.Base64.decode(LICENSE_PUBLIC_KEY,android.util.Base64.DEFAULT);
  return java.security.KeyFactory.getInstance("RSA").generatePublic(new java.security.spec.X509EncodedKeySpec(data));
 }
 long licUtcToday(){
  java.util.Calendar c=java.util.Calendar.getInstance(java.util.TimeZone.getTimeZone("America/Argentina/Buenos_Aires"));
  int y=c.get(java.util.Calendar.YEAR),m=c.get(java.util.Calendar.MONTH)+1,d=c.get(java.util.Calendar.DAY_OF_MONTH);
  return y*10000L+m*100L+d;
 }
 long licAddMonths(long time){
  java.util.Calendar c=java.util.Calendar.getInstance();
  c.setTimeInMillis(time);c.add(java.util.Calendar.MONTH,3);return c.getTimeInMillis();
 }
 android.content.SharedPreferences licPrefs(){return getSharedPreferences("nautilus_licenses_v86",MODE_PRIVATE);}
 boolean licActive(){
  long now=System.currentTimeMillis(),last=licPrefs().getLong("last_seen",0);
  if(last>now+10*60*1000L)return false;
  licPrefs().edit().putLong("last_seen",Math.max(last,now)).apply();
  long until=licPrefs().getLong("until",0);
  if(until==0){
   // Trial starts on first protected use; does not reset by closing app.
   until=licAddMonths(now);licPrefs().edit().putLong("until",until).commit();
  }
  return now<until;
 }
 boolean licAccept(String raw){
  try{
   String[] p=raw.trim().split("[.]");if(p.length!=2)return false;
   byte[] msg=android.util.Base64.decode(p[0],android.util.Base64.URL_SAFE|android.util.Base64.NO_WRAP|android.util.Base64.NO_PADDING);
   byte[] sig=android.util.Base64.decode(p[1],android.util.Base64.URL_SAFE|android.util.Base64.NO_WRAP|android.util.Base64.NO_PADDING);
   java.security.Signature verifier=java.security.Signature.getInstance("SHA256withRSA");
   verifier.initVerify(licPublicKey());verifier.update(msg);
   if(!verifier.verify(sig))return false;
   String data=new String(msg,java.nio.charset.StandardCharsets.UTF_8);
   String[] fields=data.split(":");
   if(fields.length!=3||!fields[0].equals("NTL86"))return false;
   long issued=Long.parseLong(fields[1]);
   if(issued!=licUtcToday())return false;
   String nonce=fields[2];
   if(!nonce.matches("[A-Za-z0-9_-]{12,64}"))return false;
   if(licPrefs().getBoolean("used_"+nonce,false))return false;
   long now=System.currentTimeMillis();
   return licPrefs().edit().putBoolean("used_"+nonce,true).putLong("until",licAddMonths(now)).commit();
  }catch(Exception e){return false;}
 }
 void licImportOwnerKey(){
  if(!securityOwner||!securityUnlocked)return;
  android.content.Intent i=new android.content.Intent(android.content.Intent.ACTION_OPEN_DOCUMENT);
  i.setType("*/*");i.addCategory(android.content.Intent.CATEGORY_OPENABLE);
  startActivityForResult(i,8601);
 }
 java.security.PrivateKey licOwnerKey()throws Exception{
  java.io.File f=new java.io.File(getFilesDir(),"nautilus_owner_private.pem");
  byte[] buf=new byte[(int)f.length()];
  java.io.FileInputStream in=new java.io.FileInputStream(f);
  int n=0;while(n<buf.length){int k=in.read(buf,n,buf.length-n);if(k<0)break;n+=k;}in.close();
  String pem=new String(buf,java.nio.charset.StandardCharsets.UTF_8);
  String b64=pem.replace("-----BEGIN PRIVATE KEY-----","").replace("-----END PRIVATE KEY-----","").replaceAll("\\s","");
  byte[] der=android.util.Base64.decode(b64,android.util.Base64.DEFAULT);
  return java.security.KeyFactory.getInstance("RSA").generatePrivate(new java.security.spec.PKCS8EncodedKeySpec(der));
 }
 @Override protected void onActivityResult(int request,int result,android.content.Intent data){
  super.onActivityResult(request,result,data);
  if(request!=8601)return;
  if(result!=RESULT_OK||data==null){secAdminPanel();return;}
  try{
   java.io.ByteArrayOutputStream out=new java.io.ByteArrayOutputStream();
   java.io.InputStream in=getContentResolver().openInputStream(data.getData());
   byte[] b=new byte[4096];int n,total=0;
   while((n=in.read(b))!=-1){total+=n;if(total>8192)throw new Exception("Archivo grande");out.write(b,0,n);}
   in.close();
   java.io.File f=new java.io.File(getFilesDir(),"nautilus_owner_private.pem");
   java.io.FileOutputStream file=new java.io.FileOutputStream(f);file.write(out.toByteArray());file.close();
   // Verify possession of the matching signing key, not simply the file name.
   byte[] test="NAUTILUS-PROPIETARIO".getBytes(java.nio.charset.StandardCharsets.UTF_8);
   java.security.Signature sign=java.security.Signature.getInstance("SHA256withRSA");
   sign.initSign(licOwnerKey());sign.update(test);byte[] signature=sign.sign();
   java.security.Signature check=java.security.Signature.getInstance("SHA256withRSA");
   check.initVerify(licPublicKey());check.update(test);
   if(!check.verify(signature))throw new Exception("Clave no corresponde a Nautilus");
   secPrefs().edit().putBoolean("owner_issued",true).commit();
   new AlertDialog.Builder(this).setTitle("GENERADOR HABILITADO")
    .setMessage("Tu clave coincide con Nautilus. Ya podés emitir licencias desde este teléfono.")
    .setPositiveButton("CONTINUAR",(x,y)->secAdminPanel()).show();
  }catch(Exception e){
   new java.io.File(getFilesDir(),"nautilus_owner_private.pem").delete();
   secPrefs().edit().remove("owner_issued").apply();
   new AlertDialog.Builder(this).setMessage("No se pudo validar la clave: "+e.getMessage())
    .setPositiveButton("VOLVER",(x,y)->secAdminPanel()).show();
  }
 }
 void licCreate(){
  if(!securityOwner||!securityUnlocked||!secPrefs().getBoolean("owner_issued",false))return;
  try{
   byte[] random=new byte[12];new java.security.SecureRandom().nextBytes(random);
   String nonce=android.util.Base64.encodeToString(random,android.util.Base64.URL_SAFE|android.util.Base64.NO_WRAP|android.util.Base64.NO_PADDING);
   byte[] payload=("NTL86:"+licUtcToday()+":"+nonce).getBytes(java.nio.charset.StandardCharsets.UTF_8);
   java.security.Signature sig=java.security.Signature.getInstance("SHA256withRSA");
   sig.initSign(licOwnerKey());sig.update(payload);
   String code=android.util.Base64.encodeToString(payload,android.util.Base64.URL_SAFE|android.util.Base64.NO_WRAP|android.util.Base64.NO_PADDING)
      +"."+android.util.Base64.encodeToString(sig.sign(),android.util.Base64.URL_SAFE|android.util.Base64.NO_WRAP|android.util.Base64.NO_PADDING);
   new AlertDialog.Builder(this).setTitle("LICENCIA · VÁLIDA HOY")
     .setMessage("Código válido únicamente hoy. Activará tres meses desde su ingreso.\n\n"+code)
     .setPositiveButton("COPIAR",(a,b)->{
       ((android.content.ClipboardManager)getSystemService(CLIPBOARD_SERVICE))
         .setPrimaryClip(android.content.ClipData.newPlainText("Licencia Nautilus",code));secAdminPanel();
     }).setNegativeButton("VOLVER",(a,b)->secAdminPanel()).show();
  }catch(Exception e){new AlertDialog.Builder(this).setMessage(e.toString()).setPositiveButton("VOLVER",(a,b)->secAdminPanel()).show();}
 }
 void licExpired(){
  android.widget.EditText code=new android.widget.EditText(this);
  code.setHint("Pegá el código de renovación");code.setSingleLine(false);code.setMinLines(2);
  new AlertDialog.Builder(this).setTitle("LICENCIA VENCIDA")
   .setMessage("Solicitá una nueva licencia al superadministrador. No se borrarán las fichadas.")
   .setView(code).setCancelable(false).setPositiveButton("ACTIVAR",(d,w)->{
    if(licAccept(code.getText().toString())){securityUnlocked=true;safeBootHome();}
    else new AlertDialog.Builder(this).setMessage("Código inválido, usado o emitido otro día.")
      .setCancelable(false).setPositiveButton("VOLVER",(x,y)->licExpired()).show();
   }).show();
 }
'''
s=s.replace(mark,code+'\n'+mark,1)
# Non-owner access is checked immediately before opening main screen.
needle='else if(securityOwner)secAdminPanel();else safeBootHome();'
assert needle in s
s=s.replace(needle,'else if(securityOwner)secAdminPanel();else if(licActive())safeBootHome();else licExpired();')
# Only enable owner privileges on devices provisioned with the matching private key.
# Existing installations can continue opening with their PIN, but must import
# the owner's key before issuing codes.
s=s.replace('  mtAddLink("▶","ENTRAR AL SISTEMA"', '''  mtAddLink("♧",secPrefs().getBoolean("owner_issued",false)?"GENERAR LICENCIA":"ACTIVAR GENERADOR","Licencia válida solo el día de emisión",()->{if(secPrefs().getBoolean("owner_issued",false))licCreate();else licImportOwnerKey();});
  mtAddLink("▶","ENTRAR AL SISTEMA"''',1)
p.write_text(s)
print("V86 offline verifier, trial and renewal gate installed")
