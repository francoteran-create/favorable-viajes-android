from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
s=s.replace('a.setTypeface(Typeface.DEFAULT,Typeface.BOLD);','a.setTypeface(android.graphics.Typeface.DEFAULT,android.graphics.Typeface.BOLD);')
# premiumHomeSummary already renders summary + current week in this source.
s=s.replace('premiumHomeSummary();body.addView(homeTitle("SEMANA ACTUAL"));premiumWeekStrip();','premiumHomeSummary();')
p.write_text(s);print("V58.1 compile fix")
