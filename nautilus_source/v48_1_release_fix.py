from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text().replace('h.setTypeface(null,Typeface.BOLD)','h.setTypeface(null,android.graphics.Typeface.BOLD)').replace("V48 PERSONNEL PHOTO HERO","V48.1 RELEASE COMPILE FIX")
p.write_text(s);print("V48.1 fixed Typeface compile reference")
