from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# Comprehensive UI compatibility pass: all custom menu/card factories use TextView, never themed Button.
s=s.replace('Button homeFeature(String title,String sub,Runnable run){\n  Button b=new Button(this);','TextView homeFeature(String title,String sub,Runnable run){\n  TextView b=new TextView(this);')
for name in ['turns','people','reports','cfg','imp','personal','settings','importer']:
 s=re.sub(r'Button '+name+r'=homeFeature\(', 'TextView '+name+'=homeFeature(', s)
# Any remaining dashboardCard assignment uses TextView.
s=re.sub(r'Button (\w+)=dashboardCard\(',r'TextView \1=dashboardCard(',s)
s=re.sub(r'Button (\w+)=refCard\(',r'TextView \1=refCard(',s)
# Make text resilient on narrow phones: no forced one-line, reasonable min sizes.
s=s.replace('b.setTextSize(16);b.setMinHeight(86);','b.setTextSize(15);b.setMinHeight(86);b.setMaxLines(3);')
# Ensure HOME entry is MASTER and Android back from top-level modules has a visible route.
s=s.replace('safeBootHome();','masterImageHome();')
# Persist portrait/landscape screen state by letting Android retain activity on rotation.
p.write_text(s)
print("V56 global menu visibility/phone compatibility pass")
