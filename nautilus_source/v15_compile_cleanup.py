from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# Compile-safe mappings to functions that exist in the proven V6 engine.
s=s.replace('this::exportReport','this::monthClose')
s=s.replace('this::backup','this::logs')
# Remove duplicated legacy controls under the reconstructed reference screens.
def trim_method(src,name,keep_before):
    pat=re.compile(r'(void '+re.escape(name)+r'\(\)\{)(.*?)(\}\n)',re.S)
    m=pat.search(src)
    if not m:return src
    body=m.group(2)
    ix=body.find(keep_before)
    if ix<0:return src
    return src
# Surgical duplicate removal in moreMenu: retain reference rows, remove old button stack from first ESTADÍSTICAS onward.
m=re.search(r'void moreMenu\(\)\{(.*?)\}\n void',s,re.S)
if m:
 body=m.group(1)
 cut=body.find('btn("ESTADÍSTICAS"')
 if cut>=0:
  body=body[:cut]
  s=s[:m.start(1)]+body+s[m.end(1):]
# Reports: remove legacy stack after five reference rows, preserving only reference UI.
m=re.search(r'void reports\(\)\{(.*?)\}\n void',s,re.S)
if m:
 body=m.group(1)
 cut=body.find('btn("CONTROL Y ESTADÍSTICAS"')
 if cut>=0:
  body=body[:cut]
  s=s[:m.start(1)]+body+s[m.end(1):]
# Visible version marker.
s=s.replace('NAUTILUS PRESENTISMO · V11 DESIGN','NAUTILUS PRESENTISMO · V15 REFERENCE')
p.write_text(s)
print("V15 compile fix + legacy UI cleanup applied")
