from pathlib import Path
import os
root=Path(os.environ["PROJECT"])
p=root/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# Create real Android drawable assets: dark nautical background + compact futuristic Nautilus emblem.
d=root/"app/src/main/res/drawable";d.mkdir(parents=True,exist_ok=True)
(d/"nautilus_home_bg.xml").write_text("""<layer-list xmlns:android="http://schemas.android.com/apk/res/android"><item><shape android:shape="rectangle"><gradient android:angle="270" android:startColor="#020A12" android:centerColor="#061D2C" android:endColor="#02070D"/></shape></item><item android:top="72dp"><shape><gradient android:angle="90" android:startColor="#0018273A" android:centerColor="#66213D50" android:endColor="#CC02070D"/></shape></item></layer-list>""")
(d/"nautilus_logo_futuristic.xml").write_text("""<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="124dp" android:height="124dp" android:viewportWidth="124" android:viewportHeight="124"><path android:fillColor="#061725" android:strokeColor="#36C8FF" android:strokeWidth="2" android:pathData="M62,3 A59,59 0,1 1,61.9 3"/><path android:fillColor="#0A2234" android:strokeColor="#D9A94A" android:strokeWidth="2.2" android:pathData="M62,8 A54,54 0,1 1,61.9 8"/><path android:fillColor="#1F91C4" android:pathData="M59,22 L59,69 L34,69 Z"/><path android:fillColor="#F0C56A" android:pathData="M63,17 L63,69 L88,69 Z"/><path android:fillColor="#EAF7FF" android:pathData="M61,19 L61,70 L58,70 Z"/><path android:fillColor="#D9A94A" android:pathData="M25,73 Q62,63 99,73 Q75,87 28,79 Z"/><path android:fillColor="#2DBCEB" android:pathData="M25,81 Q58,72 101,80 Q75,91 31,87 Z"/><path android:fillColor="#FFFFFF" android:pathData="M32,96 L92,96 L92,99 L32,99 Z"/><path android:fillColor="#D9A94A" android:pathData="M60,101 L64,101 L62,108 Z"/></vector>""")
mark=' void btn(String s,Runnable r){';assert mark in s
code=r'''
 android.widget.ImageView nautilusHomeLogo(){
  android.widget.ImageView logo=new android.widget.ImageView(this);logo.setImageResource(ar.com.nautiluscountry.presentismo.R.drawable.nautilus_logo_futuristic);logo.setScaleType(android.widget.ImageView.ScaleType.CENTER_INSIDE);logo.setContentDescription("Nautilus · Inicio");logo.setClickable(true);logo.setOnClickListener(v->exactToday());android.view.animation.RotateAnimation spin=new android.view.animation.RotateAnimation(0,360,android.view.animation.Animation.RELATIVE_TO_SELF,.5f,android.view.animation.Animation.RELATIVE_TO_SELF,.5f);spin.setDuration(1050);spin.setInterpolator(new android.view.animation.DecelerateInterpolator());spin.setFillAfter(true);logo.startAnimation(spin);return logo;
 }
 void applyNautilusHomeSkin(){
  try{body.setBackgroundResource(ar.com.nautiluscountry.presentismo.R.drawable.nautilus_home_bg);body.setPadding(14,8,14,22);android.widget.ImageView logo=nautilusHomeLogo();android.widget.LinearLayout.LayoutParams lp=new android.widget.LinearLayout.LayoutParams(-1,124);lp.setMargins(0,2,0,10);body.addView(logo,0,lp);}catch(Exception ignored){}
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Apply only to the real home screen after base is created.
needle='void exactToday(){'
pos=s.find(needle);assert pos>=0
brace=s.find('{',pos)+1
s=s[:brace]+'\n  applyNautilusHomeSkin();'+s[brace:]
s=s.replace("V41.1 WEEK VISUAL COMPILE FIX","V42 NAUTILUS HOME SKIN")
p.write_text(s)
print("V42 real Android background + animated home logo implemented")
