from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' java.security.PrivateKey licOwnerKey()throws Exception{'
assert mark in s
methods=r'''
 byte[] licEncryptedOwnerBytes()throws Exception{
  java.io.File file=new java.io.File(getFilesDir(),"nautilus_owner_private.enc");
  byte[] all=new byte[(int)file.length()];
  try(java.io.FileInputStream in=new java.io.FileInputStream(file)){
   int pos=0,k;
   while(pos<all.length&&(k=in.read(all,pos,all.length-pos))>0)pos+=k;
   if(pos!=all.length)throw new java.io.IOException("Clave incompleta");
  }
  if(all.length<29)throw new java.io.IOException("Clave cifrada incorrecta");
  java.security.KeyStore ks=java.security.KeyStore.getInstance("AndroidKeyStore");
  ks.load(null);
  javax.crypto.SecretKey key=(javax.crypto.SecretKey)ks.getKey("nautilus_dev_key_v99",null);
  if(key==null)throw new java.io.IOException("Clave exclusiva de este dispositivo no disponible");
  javax.crypto.Cipher cipher=javax.crypto.Cipher.getInstance("AES/GCM/NoPadding");
  cipher.init(javax.crypto.Cipher.DECRYPT_MODE,key,new javax.crypto.spec.GCMParameterSpec(128,all,0,12));
  return cipher.doFinal(all,12,all.length-12);
 }
 void licSaveEncryptedOwner(byte[] pem)throws Exception{
  java.security.KeyStore ks=java.security.KeyStore.getInstance("AndroidKeyStore");
  ks.load(null);
  if(!ks.containsAlias("nautilus_dev_key_v99")){
   javax.crypto.KeyGenerator generator=javax.crypto.KeyGenerator.getInstance("AES","AndroidKeyStore");
   generator.init(new android.security.keystore.KeyGenParameterSpec.Builder("nautilus_dev_key_v99",
    android.security.keystore.KeyProperties.PURPOSE_ENCRYPT|android.security.keystore.KeyProperties.PURPOSE_DECRYPT)
    .setBlockModes("GCM").setEncryptionPaddings("NoPadding").build());
   generator.generateKey();
  }
  javax.crypto.SecretKey key=(javax.crypto.SecretKey)ks.getKey("nautilus_dev_key_v99",null);
  javax.crypto.Cipher cipher=javax.crypto.Cipher.getInstance("AES/GCM/NoPadding");
  cipher.init(javax.crypto.Cipher.ENCRYPT_MODE,key);
  byte[] encrypted=cipher.doFinal(pem),iv=cipher.getIV();
  java.io.File f=new java.io.File(getFilesDir(),"nautilus_owner_private.enc");
  try(java.io.FileOutputStream out=new java.io.FileOutputStream(f)){
   out.write(iv);out.write(encrypted);out.getFD().sync();
  }
 }
'''
s=s.replace(mark,methods+mark,1)
old='''  java.io.File f=new java.io.File(getFilesDir(),"nautilus_owner_private.pem");
  byte[] buf=new byte[(int)f.length()];
  java.io.FileInputStream in=new java.io.FileInputStream(f);
  int n=0;while(n<buf.length){int k=in.read(buf,n,buf.length-n);if(k<0)break;n+=k;}in.close();'''
assert old in s
s=s.replace(old,'''  byte[] buf=licEncryptedOwnerBytes();''',1)
old='''   java.io.File f=new java.io.File(getFilesDir(),"nautilus_owner_private.pem");
   java.io.FileOutputStream file=new java.io.FileOutputStream(f);file.write(out.toByteArray());file.close();'''
assert old in s
s=s.replace(old,'''   licSaveEncryptedOwner(out.toByteArray());''',1)
s=s.replace('new java.io.File(getFilesDir(),"nautilus_owner_private.pem").delete();','new java.io.File(getFilesDir(),"nautilus_owner_private.enc").delete();')
p.write_text(s)
print("V99 encrypt developer signing key with AndroidKeyStore AES-GCM")
