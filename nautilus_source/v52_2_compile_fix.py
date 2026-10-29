from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
s=s.replace('body.addView(homeTitle("SEMANA ACTUAL")); premiumHomeWeek();','')
# premiumHomeSummary already renders RESUMEN DEL MES and SEMANA ACTUAL, so avoid duplicates too
s=s.replace('body.addView(homeTitle("RESUMEN DEL MES"));premiumHomeSummary();','premiumHomeSummary();')
p.write_text(s);print("V52.2 uses existing real summary/week renderer")
