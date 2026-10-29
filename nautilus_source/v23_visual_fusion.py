from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
s=s.replace('Typeface.DEFAULT,Typeface.BOLD','android.graphics.Typeface.DEFAULT,android.graphics.Typeface.BOLD')
# Determine employeeProfile parameter and repair metric strip call.
m=re.search(r'void employeeProfile\(String\s+(\w+)\)',s)
if m:
    param=m.group(1)
    # replace only call in profile vicinity; id is invalid there
    pos=s.find('void employeeProfile(')
    end=s.find('void ',pos+10)
    seg=s[pos:end]
    seg=seg.replace('employeeMetricStrip(id);',f'employeeMetricStrip({param});')
    s=s[:pos]+seg+s[end:]
# Sector premium hero.
s=s.replace('base(sector);body.addView(statusPill("COBERTURA DEL SECTOR"', 'base(sector);body.addView(refHero(sector,"Cobertura operativa del sector"));body.addView(statusPill("COBERTURA DEL SECTOR"')
# Incidents hero if exact method signature present.
s=s.replace('void incidentsReference(){base("INCIDENCIAS");','void incidentsReference(){base("INCIDENCIAS");body.addView(refHero("INCIDENCIAS","Tardanzas · ausencias · marcaciones"));')
# Calendar hero.
s=s.replace('void calendarMonth(){currentScreen="TURNOS";base("TURNOS");','void calendarMonth(){currentScreen="TURNOS";base("TURNOS");body.addView(refHero("TURNOS","Calendario de trabajo y francos"));')
s=s.replace('V22 VISUAL REACTOR','V23 VISUAL FUSION')
p.write_text(s)
print("V23 visual fusion repair applied")
