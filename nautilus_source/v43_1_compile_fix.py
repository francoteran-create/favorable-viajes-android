from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text().replace('this::exactPeople','this::employees').replace("V43 PREMIUM HOME","V43.1 PREMIUM HOME FIX")
p.write_text(s);print("V43.1 personnel route fixed")
