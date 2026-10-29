from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
m=re.search(r'\bvoid\s+safeBootHome\s*\(\s*\)\s*\{',s)
assert m,"safeBootHome missing"
start=m.end();depth=1;i=start
while depth:
 if s[i]=="{":depth+=1
 elif s[i]=="}":depth-=1
 i+=1
body=s[start:i-1]
assert "mtAddLink" not in body or "PANEL DESARROLLADOR" not in body
insert='''
  if(securityOwner&&securityUnlocked&&licDeveloperAuthorized()){
   mtAddLink("⚙","VOLVER AL PANEL DESARROLLADOR","Administrar usuarios y generar licencias",this::secAdminPanel);
  }
'''
s=s[:i-1]+insert+s[i-1:]
p.write_text(s)
print("V105 developer return button on main presentismo landing")
