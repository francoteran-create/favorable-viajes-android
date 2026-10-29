from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
for marker in ['CREATE TABLE IF NOT EXISTS punches','CREATE TABLE punches','int importClock(InputStream','void importedPunchHistory()','void pick(){','void onActivityResult(']:
 at=s.find(marker)
 print("DIAG MARK",marker,at,("\n"+s[max(0,at-160):at+4400]) if at>=0 else "")
# Keep source unchanged on diagnostic build
