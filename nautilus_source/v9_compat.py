from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# navigation state
if 'String currentScreen=' not in s:
 s=s.replace('static final int PICK=12, SAVE_REPORT=13;','static final int PICK=12, SAVE_REPORT=13; String currentScreen="HOY";')
# Adapt newer analytics layer to the proven V6 engine API.
s=s.replace('dayResult(pid,day)','calcDay(pid,day)')
s=s.replace('dayResult(pid,String.format(Locale.US,"%s-%02d",ym,d))','calcDay(pid,String.format(Locale.US,"%s-%02d",ym,d))')
s=s.replace('r.present','r.worked>0')
s=s.replace('r.lateMinutes','r.late')
s=s.replace('r.clockMinutes','r.worked')
# recognized minutes are review-aware; use engine helper with the current day where available.
s=s.replace('r.recognizedMinutes','recognized(pid,day,r)')
p.write_text(s)
print("V9 compatibility applied")
