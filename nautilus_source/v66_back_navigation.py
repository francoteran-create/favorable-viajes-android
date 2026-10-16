from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# Explicit Back handling rather than V62's conditional insertion (which can skip legacy overrides).
pattern=r'@Override\s+public\s+void\s+onBackPressed\s*\(\s*\)\s*\{'
m=re.search(pattern,s)
if m:
 start=s.index('{',m.start());depth=0;end=None
 for i in range(start,len(s)):
  if s[i]=='{':depth+=1
  elif s[i]=='}':
   depth-=1
   if depth==0:end=i+1;break
 assert end is not None
 s=s[:m.start()]+s[end:]
mark=' void btn(String s,Runnable r){'
assert mark in s
handler=r'''
 @Override public void onBackPressed(){
  if("INICIO".equals(currentScreen)){super.onBackPressed();return;}
  // Historical dashboard HOY is no longer a destination; Back returns to MASTER.
  masterImageHomeV59();
 }
'''
s=s.replace(mark,handler+mark,1)
# Reconcile all native screens' currentScreen with the tab selected, when an older screen doesn't set it.
# The main screen already sets INICIO explicitly.
s=s.replace('void mtScreen(String title,int selected){','void mtScreen(String title,int selected){\n  if(selected==0&&!"INICIO".equals(currentScreen))currentScreen="SUBPANTALLA";',1)
p.write_text(s)
print("V66 explicit Android back behavior: submodules -> MASTER, no old HOY")
