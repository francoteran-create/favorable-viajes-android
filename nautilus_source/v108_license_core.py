from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
core=Path(__file__).with_name("license_core")/"OfflineLicenseCore.java"
destination=p.with_name("OfflineLicenseCore.java")
destination.write_bytes(core.read_bytes())
old=''' long licAddMonths(long time){
  java.util.Calendar c=java.util.Calendar.getInstance();
  c.setTimeInMillis(time);c.add(java.util.Calendar.MONTH,3);return c.getTimeInMillis();
 }'''
assert old in s,"Existing calendar logic changed"
s=s.replace(old,''' long licAddMonths(long time){
  return OfflineLicenseCore.addMonths(time);
 }''',1)
old='''   java.security.Signature verifier=java.security.Signature.getInstance("SHA256withRSA");
   verifier.initVerify(licPublicKey());verifier.update(msg);
   if(!verifier.verify(sig))return false;
   String data=new String(msg,java.nio.charset.StandardCharsets.UTF_8);
   String[] fields=data.split(":");
   if(fields.length!=3||!fields[0].equals("NTL86"))return false;
   long issued=Long.parseLong(fields[1]);
   if(issued!=licUtcToday())return false;
   String nonce=fields[2];
   if(!nonce.matches("[A-Za-z0-9_-]{12,64}"))return false;'''
assert old in s,"Existing signature gate changed"
s=s.replace(old,'''   String nonce=OfflineLicenseCore.verify(msg,sig,licPublicKey(),licUtcToday());
   if(nonce==null)return false;''',1)
old='''   byte[] payload=("NTL86:"+licUtcToday()+":"+nonce).getBytes(java.nio.charset.StandardCharsets.UTF_8);'''
assert old in s,"Existing license generator changed"
s=s.replace(old,'''   byte[] payload=OfflineLicenseCore.payload(licUtcToday(),nonce);''',1)
p.write_text(s)
print("V108: Android now invokes the independently testable license core")
