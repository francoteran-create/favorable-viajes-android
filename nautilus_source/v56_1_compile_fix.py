from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# Exhaustive declaration cleanup for helpers converted from Button to TextView.
for helper in ["homeFeature","dashboardCard","refCard"]:
 s=re.sub(r'Button\s+(\w+)\s*=\s*'+helper+r'\(',r'TextView \1='+helper+'(',s)
p.write_text(s);print("V56.1 exhaustive card type cleanup")
