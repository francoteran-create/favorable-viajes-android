from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# V39: runtime root-cause repair. Original DB schema stores sector_id, while the
# new visual/personnel screens query people.sector. Add the compatibility column
# and backfill it from sectors BEFORE any exact/live screen queries it.
s=s.replace('String[] cols={"dni TEXT","cuil TEXT","phone TEXT","address TEXT","birth_date TEXT","hire_date TEXT","job_title TEXT","emergency_contact TEXT","photo_uri TEXT","notes TEXT"};',
'''String[] cols={"sector TEXT","dni TEXT","cuil TEXT","phone TEXT","address TEXT","birth_date TEXT","hire_date TEXT","job_title TEXT","emergency_contact TEXT","photo_uri TEXT","notes TEXT"};''')
needle='for(String def:cols){try{x.execSQL("ALTER TABLE people ADD COLUMN "+def);}catch(Exception ignored){}}'
replacement=needle+'''
  try{x.execSQL("UPDATE people SET sector=(SELECT name FROM sectors WHERE sectors.id=people.sector_id) WHERE (sector IS NULL OR trim(sector)='') AND sector_id IS NOT NULL");}catch(Exception ignored){}'''
s=s.replace(needle,replacement)
# Guarantee schema compatibility at entry to every new shell, after db has been initialized.
s=s.replace('void exactToday(){\n  currentScreen="HOY";','void exactToday(){\n  ensurePersonnelMaster();\n  currentScreen="HOY";')
s=s.replace('V38 STARTUP HARDENING','V39 RUNTIME SCHEMA REPAIR')
p.write_text(s)
print("V39 runtime schema compatibility repair applied")
