from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# Remaining V43 declarations after helper changed to TextView.
s=re.sub(r'Button (personal|reports|settings|importer)=dashboardCard\(',r'TextView \1=dashboardCard(',s)
p.write_text(s);print("V55.1 compile type cleanup")
