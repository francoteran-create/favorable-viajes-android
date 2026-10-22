from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text();mark=' void btn(String s,Runnable r){';assert mark in s
helper=r'''
 Button weekNavBtn(String text){
  Button b=new Button(this);b.setText(text);b.setTextColor(Color.WHITE);b.setTextSize(11);b.setAllCaps(false);b.setGravity(Gravity.CENTER);b.setBackground(refBg(Color.rgb(8,38,52),Color.rgb(42,91,110),18));return b;
 }
'''
s=s.replace(mark,helper+"\n"+mark).replace('miniBtn("‹ SEMANA")','weekNavBtn("‹ SEMANA")').replace('miniBtn("HOY")','weekNavBtn("HOY")').replace('miniBtn("SEMANA ›")','weekNavBtn("SEMANA ›")')
# stronger visual hierarchy: taller week cards, gold selected state, larger type through existing rows
s=s.replace('card.setMinimumHeight(86);','card.setMinimumHeight(104);')
s=s.replace("V41 WEEK PLANNING","V41.1 WEEK VISUAL COMPILE FIX")
p.write_text(s);print("V41.1 visual/navigation compile repair applied")
