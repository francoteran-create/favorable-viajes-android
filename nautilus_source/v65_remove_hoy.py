from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
def replace_method(source,name,body):
 m=re.search(r'\bvoid\s+'+re.escape(name)+r'\s*\(\s*\)\s*\{',source)
 if not m:return source,False
 start=source.index('{',m.start());depth=0;quote=None;escape=False
 for i in range(start,len(source)):
  c=source[i]
  if quote:
   if escape:escape=False
   elif c=='\\':escape=True
   elif c==quote:quote=None
   continue
  if c in ['"',"'"]:quote=c;continue
  if c=='{':depth+=1
  if c=='}':
   depth-=1
   if depth==0:return source[:m.start()]+'void '+name+'(){'+body+'}'+source[i+1:],True
 raise RuntimeError("Unclosed "+name)
for name in ["exactToday","home","safeBootHome"]:
 s,ok=replace_method(s,name,"masterImageHomeV59();")
 print(name,ok)
# Never show older day-only dashboard from launch/nav; use the modern MASTER.
s=s.replace('this::exactToday','this::masterImageHomeV59')
s=s.replace('this::home','this::masterImageHomeV59')
# Change the one legacy button into a modern direct link if anyone reaches its screen.
s=s.replace('btn("ABRIR ALMANAQUE",()->mtCalendar(new Date()));','btn("VER CALENDARIO MENSUAL",()->mtCalendar(new Date()));')
p.write_text(s)
print("V65 old HOY operational screen retired, all main paths to MASTER")
