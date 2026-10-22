from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# Kill the visible V49 diagnostic boot: retain uncaught-exception recorder, but boot directly into approved MASTER home.
start=s.find("protected void onCreate(")
if start<0: start=s.find("public void onCreate(")
end=s.find("\n }",start)
block=s[start:end]
block=block.replace("safeBootHome();","masterImageHome();")
s=s[:start]+block+s[end:]
# Any legacy HOME/Hoy bottom target is redirected to MASTER.
s=s.replace('this::exactToday','this::masterImageHome')
# Make old calendar entry route to the readable weekly planner.
s=s.replace('this::calendarMonth','()->weekPlanner(new Date())')
s=s.replace("V52 MASTER IMAGE HOME","V53 MASTER COMPONENTS ONLY")
p.write_text(s)
print("V53: visible safe boot removed; MASTER home is launcher; legacy home/calendar routes redirected")
