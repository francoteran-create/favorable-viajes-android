from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void dualClockHub(){'
assert mark in s
code=r'''
 // V86: Offline licensing. Private signing key is not shipped in distributed APK.
 static final String LICENSE_PUBLIC_KEY="PUBLIC_KEY_PLACEHOLDER";
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
p.write_text(s)
print("V86 offline verifier, trial and renewal gate installed")
