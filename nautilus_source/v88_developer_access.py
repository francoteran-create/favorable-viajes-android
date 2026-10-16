from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# Consistent user-facing wording and one-second splash.
for before,after in [
 ("SUPERADMINISTRADOR","DESARROLLADOR"),
 ("SUPERADMIN · USUARIOS","PANEL DEL DESARROLLADOR"),
 ("superadministrador","desarrollador"),
 ("Superadministrador","Desarrollador"),
 ("},500);","},1000);")
]:
 s=s.replace(before,after)
# A clean recipient installation must not self-provision unlimited access.
needle='if(index==0&&!secPrefs().contains(user+"_hash")){secEnroll();return;}'
assert needle in s
s=s.replace(needle,'''if(index==0&&!secPrefs().contains(user+"_hash")){
   new AlertDialog.Builder(this).setTitle("DESARROLLADOR")
    .setMessage("Este teléfono no está configurado como dispositivo del desarrollador.")
    .setCancelable(false).setPositiveButton("VOLVER",(x,y)->secLogin()).show();return;
  }''')
# New installs run splash too, not only returning users.
needle='if(!secPrefs().contains("owner_hash")){secLogin();return;}'
assert needle in s
s=s.replace(needle,'if(!secPrefs().contains("owner_hash")){secSplash();return;}',1)
# Password-free option must not evade three-month expiration.
needle='if(secPrefs().getBoolean("skip_"+user,false)){securityUnlocked=true;securityOwner=index==0;securityPromptOpen=false;if(index==0&&!secPrefs().getBoolean("owner_pin",false))secOwnerPin();else if(securityOwner)secAdminPanel();else if(licActive())safeBootHome();else licExpired();return;}'
assert needle in s
s=s.replace(needle,'''if(secPrefs().getBoolean("skip_"+user,false)){
   securityUnlocked=true;securityOwner=index==0;securityPromptOpen=false;
   if(securityOwner&&!secPrefs().getBoolean("owner_issued",false)){securityUnlocked=false;secLogin();return;}
   if(securityOwner)secAdminPanel();else if(licActive())safeBootHome();else licExpired();return;
  }''',1)
# Existing unprovisioned owner is not an unlimited bypass.
needle='if(index==0&&!secPrefs().getBoolean("owner_pin",false))secOwnerPin();else if(securityOwner)secAdminPanel();else if(licActive())safeBootHome();else licExpired();'
assert needle in s
s=s.replace(needle,'''if(index==0&&!secPrefs().getBoolean("owner_pin",false))secOwnerPin();
     else if(securityOwner)secAdminPanel();
     else if(licActive())safeBootHome();else licExpired();''')
p.write_text(s)
print("V88 role labels, 1000ms splash, no fresh owner bypass, trial-safe remembered login")
