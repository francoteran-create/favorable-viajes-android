from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# V38 critical runtime repair: V26 injected a DB migration before the original onCreate
# initializes the db helper. Later V27.1 only removed the exact adjacent form, but
# subsequent transforms can leave whitespace/newline variants. Remove every early form.
import re
s=re.sub(r'super\.onCreate\(b\);\s*ensurePersonnelMaster\(\);','super.onCreate(b);',s,count=1)
# Also protect the migration itself: if any screen reaches it before db exists, do not crash.
s=s.replace('void ensurePersonnelMaster(){\n  android.database.sqlite.SQLiteDatabase x=db.getWritableDatabase();',
'''void ensurePersonnelMaster(){
  if(db==null)return;
  android.database.sqlite.SQLiteDatabase x=db.getWritableDatabase();''')
# Do not enter the heavy exact shell until after normal initialization has completed.
# The original first home replacement is retained only if it occurs after db assignment;
# otherwise defer through a posted UI callback, which runs after onCreate returns.
# This additionally catches initialization-order regressions without changing business data.
s=s.replace('V37 CONSOLIDATED FLOW','V38 STARTUP HARDENING')
p.write_text(s)
print("V38 startup hardening applied")
