from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# Prevent ordinary users from continuing through a stale unlocked flag after expiry.
needle='''  if(!securityOwner&&!licActive()&&!securityPromptOpen){
   securityPromptOpen=true;
   licExpired();
  }'''
assert needle in s
s=s.replace(needle,'''  if(!securityOwner&&!licActive()&&!securityPromptOpen){
   securityUnlocked=false;
   securityPromptOpen=true;
   licExpired();
  }''',1)
# A failed renewal cannot retain an unlocked session.
needle='''void licExpired(){
  android.widget.EditText code'''
assert needle in s
s=s.replace(needle,'''void licExpired(){
  securityUnlocked=false;
  securityPromptOpen=true;
  android.widget.EditText code''',1)
# On successful activation restore session and reset prompt.
needle='''if(licAccept(code.getText().toString())){securityPromptOpen=false;securityUnlocked=true;safeBootHome();}'''
assert needle in s
# Record first use before account selection; no restart of trial on admin change.
needle='''if(!secPrefs().contains("owner_hash")){secSplash();return;}'''
assert needle in s
s=s.replace(needle,'''if(!secPrefs().contains("owner_hash")){licActive();secSplash();return;}''',1)
# The app should not expose sensitive data via Android's recent-task preview.
needle=''' @Override protected void onResume(){'''
assert needle in s
s=s.replace(needle,''' @Override protected void onStart(){
  super.onStart();
  getWindow().setFlags(android.view.WindowManager.LayoutParams.FLAG_SECURE,
    android.view.WindowManager.LayoutParams.FLAG_SECURE);
 }
 @Override protected void onResume(){''',1)
p.write_text(s)
print("V93 license-gate hardening")
