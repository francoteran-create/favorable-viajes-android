from pathlib import Path
import os, base64
root=Path(os.environ["PROJECT"])
java=root/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
drawable=root/"app/src/main/res/drawable"
drawable.mkdir(parents=True,exist_ok=True)
(drawable/"proyecto_cero_splash.jpg").write_bytes(base64.b64decode((Path(__file__).with_name("v84_splash.b64")).read_text().strip()))
s=java.read_text()
assert 'void secLogin(){' in s
assert 'if(!secPrefs().contains("owner_hash")){secEnroll();return;}' in s
s=s.replace('if(!secPrefs().contains("owner_hash")){secEnroll();return;}\n  secLogin();',
'''if(!secPrefs().contains("owner_hash")){secEnroll();return;}
  secSplash();''',1)
code=r'''
 void secSplash(){
  securityPromptOpen=true;
  android.widget.ImageView art=new android.widget.ImageView(this);
  art.setImageResource(ar.com.nautiluscountry.presentismo.R.drawable.proyecto_cero_splash);
  art.setScaleType(android.widget.ImageView.ScaleType.CENTER_CROP);
  final android.app.Dialog splash=new android.app.Dialog(this,android.R.style.Theme_Black_NoTitleBar_Fullscreen);
  splash.setContentView(art);splash.setCancelable(false);splash.show();
  new android.os.Handler(android.os.Looper.getMainLooper()).postDelayed(()->{
   if(!isFinishing()&&splash.isShowing()){splash.dismiss();secLogin();}
  },500);
 }
'''
mark=' void secLogin(){'
s=s.replace(mark,code+mark,1)
java.write_text(s)
print("V84: splash photograph, 500 ms, then account selection")
