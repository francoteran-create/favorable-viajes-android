from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# Critical startup crash repair: V26 called ensurePersonnelMaster() immediately after super.onCreate,
# before db is initialized by the original activity.
s=s.replace('super.onCreate(b);ensurePersonnelMaster();','super.onCreate(b);')
# ensure schema lazily only from screens/actions after db initialization.
s=s.replace('V27 TOUCH CALENDAR','V27.1 STARTUP HOTFIX')
p.write_text(s)
print("V27.1 removed premature DB access from onCreate")
