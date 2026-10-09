from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
s=s.replace('new SimpleDateFormat("EEEE d \'de\' MMMM",new Locale("es","AR")).format(parse(day))','day')
s=s.replace('sectionTitle("TRABAJA / FRANCO / LICENCIA / INCIDENCIAS");','sectionTitle("DIAGRAMA DEL MES","TRABAJA · FRANCO · LICENCIA · INCIDENCIAS");')
# Add a stronger expected-roster heading to day screen. calcDay is the authoritative diagram engine.
s=s.replace('Cursor c=db.getReadableDatabase().rawQuery("SELECT id,name,sector FROM people WHERE active=1 ORDER BY sector,name",null);','sectionTitle("PERSONAL PROGRAMADO","Según el diagrama previamente cargado");Cursor c=db.getReadableDatabase().rawQuery("SELECT id,name,sector FROM people WHERE active=1 ORDER BY sector,name",null);',1)
s=s.replace('V24 CALENDAR PEOPLE','V25 DIAGRAM ROSTER')
p.write_text(s)
print("V25 diagram roster compile repair applied")
