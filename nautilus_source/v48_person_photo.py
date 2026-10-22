from pathlib import Path
import os
root=Path(os.environ["PROJECT"]);p=root/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java";s=p.read_text()
mark=' void btn(String s,Runnable r){';assert mark in s
code=r'''
 void premiumEmployeePhoto(String pid){
  try{String[] a=personMaster(pid);String uri=a.length>11?a[11]:null;ImageView photo=new ImageView(this);photo.setScaleType(ImageView.ScaleType.CENTER_CROP);photo.setBackgroundResource(ar.com.nautiluscountry.presentismo.R.drawable.nautilus_glass_card);if(uri!=null&&!uri.trim().isEmpty()){try{photo.setImageURI(android.net.Uri.parse(uri));}catch(Exception ignored){photo.setImageResource(android.R.drawable.ic_menu_camera);}}else photo.setImageResource(android.R.drawable.ic_menu_camera);photo.setContentDescription("Foto del empleado · tocar para agregar o cambiar");photo.setOnClickListener(v->pickEmployeePhoto(pid));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,190);lp.setMargins(0,8,0,10);body.addView(photo,Math.min(3,body.getChildCount()),lp);TextView hint=label(uri==null||uri.trim().isEmpty()?"AGREGAR FOTO":"TOCAR FOTO PARA CAMBIAR",10);hint.setGravity(Gravity.CENTER);hint.setTextColor(Color.rgb(224,181,79));body.addView(hint,Math.min(4,body.getChildCount()));}catch(Exception ignored){}
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Add real photo hero to exactPersonal after base creation.
i=s.find("void exactPersonal(")
if i>=0:
 j=s.find("base(",i);e=s.find(";",j)+1
 # derive pid argument name is expected pid in current implementation
 s=s[:e]+'premiumEmployeePhoto(pid);'+s[e:]
s=s.replace("V47 UNIFIED PREMIUM MODULES","V48 PERSONNEL PHOTO HERO")
p.write_text(s);print("V48 employee real-photo hero implemented")
