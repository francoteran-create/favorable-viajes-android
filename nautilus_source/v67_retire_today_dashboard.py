from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
def replace_method(src,name,params,impl):
 pat=r'\bvoid\s+'+re.escape(name)+r'\s*\('+params+r'\)\s*\{'
 m=re.search(pat,src)
 if not m:print("No method",name);return src
 st=src.index('{',m.start());depth=0;quote=None;esc=False
 for j in range(st,len(src)):
  c=src[j]
  if quote:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c==quote:quote=None
   continue
  if c in ['"',"'"]:quote=c;continue
  if c=='{':depth+=1
  elif c=='}':
   depth-=1
   if depth==0:
    return src[:m.start()]+'void '+name+'('+('' if not params else params.replace(r'\s*',''))+'){'+impl+'}'+src[j+1:]
 raise RuntimeError("Unclosed method "+name)
# The legacy 'HOY' screen is actually todayDashboard(), not exactToday().
s=replace_method(s,'todayDashboard','', 'masterImageHomeV59();')
# Legacy in-screen "VOLVER" links still exist; they must not restore old dashboard.
s=replace_method(s,'back','', 'btn("← INICIO",this::masterImageHomeV59);')
# Legacy navigation callbacks still referencing old dashboard are sent to MASTER.
s=s.replace('this::todayDashboard','this::masterImageHomeV59')
s=s.replace('todayDashboard();','masterImageHomeV59();')
# Keep the import/attendance logic; only remove the old HOY presentation.
# Show a small build identifier in CONFIG so installation can be confirmed in screenshots.
needle='void mtConfig(){\n  currentScreen="CONFIG";mtScreen("CONFIGURACIÓN",4);'
if needle in s:
 s=s.replace(needle,needle+'\n  body.addView(mtText("NAUTILUS V67 · NAVEGACIÓN MASTER",11,mtPale(),true));',1)
p.write_text(s)
print("V67 explicitly retires actual legacy todayDashboard, back links, and adds installed-build marker")
