from pathlib import Path
import os
root=Path(os.environ["PROJECT"])
j=root/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=j.read_text()
mark=' void licExpired(){'
assert mark in s
addition=r'''
 boolean licDeveloperAuthorized(){
  try{
   byte[] challenge=new byte[32];new java.security.SecureRandom().nextBytes(challenge);
   java.security.Signature signer=java.security.Signature.getInstance("SHA256withRSA");
   signer.initSign(licOwnerKey());signer.update(challenge);
   byte[] proof=signer.sign();
   java.security.Signature verify=java.security.Signature.getInstance("SHA256withRSA");
   verify.initVerify(licPublicKey());verify.update(challenge);
   return verify.verify(proof);
  }catch(Exception ex){return false;}
 }
'''
s=s.replace(mark,addition+mark,1)
# A mutable preference flag alone must not confer developer powers.
s=s.replace('secPrefs().getBoolean("owner_issued",false)', 'licDeveloperAuthorized()')
# Keep previous owner role blocked if key isn't present or mismatches.
s=s.replace('if(securityOwner)secAdminPanel();','if(securityOwner&&licDeveloperAuthorized())secAdminPanel();else if(securityOwner){securityUnlocked=false;secLogin();}',1)
# Lock down developer menu reachable from elsewhere, not only login.
s=s.replace('if(!securityOwner||!securityUnlocked){secGate();return;}','if(!securityOwner||!securityUnlocked||!licDeveloperAuthorized()){secGate();return;}')
j.write_text(s)
# Sensitive local login / licensing preferences must never be Android cloud backed up or transferred.
manifest=root/"app/src/main/AndroidManifest.xml"
if manifest.exists():
 m=manifest.read_text()
 m=m.replace('android:allowBackup="true"','android:allowBackup="false" android:fullBackupContent="false" android:dataExtractionRules="@xml/nautilus_data_extraction"')
 manifest.write_text(m)
 xml=root/"app/src/main/res/xml/nautilus_data_extraction.xml"
 xml.parent.mkdir(parents=True,exist_ok=True)
 xml.write_text("""<?xml version="1.0" encoding="utf-8"?>
<data-extraction-rules xmlns:android="http://schemas.android.com/apk/res/android">
 <cloud-backup><exclude domain="root" path="."/></cloud-backup>
 <device-transfer><exclude domain="root" path="."/></device-transfer>
</data-extraction-rules>
""")
print("V90 proof-of-possession developer guard + disable app data backups")
