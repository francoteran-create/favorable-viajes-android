from pathlib import Path
import os
root=Path(os.environ["PROJECT"]);p=root/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java";s=p.read_text()
mark=' void btn(String s,Runnable r){';assert mark in s
code=r'''
 void applyPremiumModuleSkin(String kicker,String title,String sub){
  try{body.setBackgroundResource(ar.com.nautiluscountry.presentismo.R.drawable.nautilus_home_bg);body.setPadding(14,10,14,24);TextView k=label(kicker,10);k.setTextColor(Color.rgb(224,181,79));k.setLetterSpacing(.18f);body.addView(k,0);TextView h=label(title,26);h.setTextColor(Color.WHITE);h.setTypeface(null,Typeface.BOLD);body.addView(h,1);TextView d=label(sub,12);d.setTextColor(Color.rgb(157,188,201));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,-2);lp.setMargins(0,0,0,12);body.addView(d,2,lp);}catch(Exception ignored){}
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Apply same identity to weekly turns and employee list, immediately after their base screen creation.
# Transformers run on final generated Java, so target method openings and first base(...) call locally.
def inject(method,call):
 global s
 i=s.find(method)
 if i<0:return
 j=s.find("base(",i)
 if j<0:return
 e=s.find(";",j)+1
 s=s[:e]+call+s[e:]
inject("void exactWeekTurns(","applyPremiumModuleSkin(\"PLANIFICACIÓN\",\"TURNOS\",\"Semana visible · lunes a domingo\");")
inject("void employees()","applyPremiumModuleSkin(\"NAUTILUS COUNTRY\",\"PERSONAL\",\"Ficha maestra · sector · régimen · estadísticas\");")
s=s.replace("V46 PREMIUM NAV","V47 UNIFIED PREMIUM MODULES")
p.write_text(s);print("V47 unified premium identity applied to Turns + Personnel")
