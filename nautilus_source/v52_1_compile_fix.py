from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
s=s.replace('v.setTypeface(Typeface.DEFAULT,Typeface.BOLD);','v.setTypeface(android.graphics.Typeface.DEFAULT,android.graphics.Typeface.BOLD);')
s=s.replace('body.addView(homeTitle("SEMANA ACTUAL"));premiumWeekStrip();','body.addView(homeTitle("SEMANA ACTUAL")); premiumHomeWeek();')
p.write_text(s);print("V52.1 compile fix")
