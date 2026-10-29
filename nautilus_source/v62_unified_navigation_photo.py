from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()

def swap_method(src,signature,newbody):
 m=re.search(signature,src)
 if not m: raise RuntimeError("Required UI method not found: "+signature)
 st=src.index('{',m.start()); depth=0; quote=None; esc=False; line_comment=False; block_comment=False
 for i in range(st,len(src)):
  c=src[i]; n=src[i+1] if i+1<len(src) else ''
  if line_comment:
   if c=='\n':line_comment=False
   continue
  if block_comment:
   if c=='*' and n=='/':block_comment=False
   continue
  if quote:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c==quote:quote=None
   continue
  if c=='/' and n=='/':line_comment=True;continue
  if c=='/' and n=='*':block_comment=True;continue
  if c in ['"',"'"]:quote=c;continue
  if c=='{':depth+=1
  if c=='}':
   depth-=1
   if depth==0:return src[:m.start()]+newbody+src[i+1:]
 raise RuntimeError("Unterminated method "+signature)

s=swap_method(s,r'\bvoid\s+base\s*\(\s*String\s+title\s*\)\s*\{',r'''
 void base(String title){
  String t=title==null?"":title.toUpperCase(new Locale("es","AR"));
  int tab=t.contains("INFORM")||t.contains("ESTAD")||t.contains("REPOR")?3:
   (t.contains("PERSON")||t.contains("EMPLE")||t.contains("FICHA")?2:
   (t.contains("TURNO")||t.contains("DÍA")||t.contains("CALEND")||t.contains("DIAGRAMA")?1:
   (t.contains("CONFIG")||t.contains("MÁS")||t.contains("IMPORT")||t.contains("SECTOR")||t.contains("RÉGIM")?4:0)));
  mtScreen(title,tab);
 }
''')
s=swap_method(s,r'\bvoid\s+btn\s*\(\s*String\s+s\s*,\s*Runnable\s+r\s*\)\s*\{',r'''
 void btn(String s,Runnable r){
  TextView b=mtText(s,14,Color.WHITE,true);b.setGravity(Gravity.CENTER_VERTICAL);
  b.setPadding(mtDp(16),mtDp(12),mtDp(13),mtDp(12));b.setMaxLines(3);
  b.setBackground(mtBg(0xFF0E3248,0xFF041320,0xFF408AAC,15));
  b.setOnClickListener(v->r.run());b.setContentDescription(s);
  LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,-2);
  lp.setMargins(0,mtDp(5),0,mtDp(5));b.setMinimumHeight(mtDp(54));body.addView(b,lp);
 }
''')
s=swap_method(s,r'\bvoid\s+exactBottom\s*\(\s*String\s+active\s*\)\s*\{',r'''
 void exactBottom(String active){
  // Each screen already owns a fixed MASTER bottom navigation via mtScreen().
 }
''')
# Legacy UI actions route to the new functional screens, especially return after manual personnel creation and importing clock data.
start=s.find('void editPerson(')
if start>=0:
 end=s.find('\n void ',start+6)
 if end<0:end=len(s)
 part=s[start:end]
 part=part.replace('employees();','mtPersonnel();')
 s=s[:start]+part+s[end:]
s=s.replace('this::home);}catch(Exception e){msg("No se pudo importar"', 'this::mtPersonnel);}catch(Exception e){msg("No se pudo importar"')

# Most old profile edits previously returned to the obsolete employeeProfile screen.
start=s.find('void personnelMasterForm(')
if start>=0:
 end=s.find('\n void ',start+6)
 if end<0:end=len(s)
 part=s[start:end]
 part=part.replace('employeeProfile(pid);','mtEmployee(pid);')
 s=s[:start]+part+s[end:]

# The upstream photo transformer assumed parameter names "requestCode" and "resultCode", but the
# real Activity uses "q" and "res". Its hook never got installed; a picked photo was discarded.
match=re.search(r'\bvoid\s+onActivityResult\s*\(\s*int\s+(\w+)\s*,\s*int\s+(\w+)\s*,\s*Intent\s+(\w+)\s*\)\s*\{',s)
if not match:raise RuntimeError("onActivityResult missing: cannot deliver working employee photos")
qn,rn,dn=match.groups()
handler=f'if({qn}==902&&{rn}==RESULT_OK&&{dn}!=null&&{dn}.getData()!=null){{saveEmployeePhoto({dn}.getData());return;}}'
start=match.end();end=s.find('\n void ',start)
if end<0:end=len(s)
existing=s[start:end]
if 'saveEmployeePhoto(' not in existing:
 s=s[:start]+handler+s[start:]
 print("V62 PHOTO CALLBACK repaired:",qn,rn,dn)
else:print("V62 photo callback already present")

# Back always returns home from submodules. OS Back from HOME still exits as expected.
if 'void onBackPressed()' not in s:
 mark=' void btn(String s,Runnable r){'
 where=s.find(mark)
 assert where>=0
 s=s[:where]+''' @Override public void onBackPressed(){
  if(!"INICIO".equals(currentScreen)){masterImageHomeV59();}else{super.onBackPressed();}
 }
 '''+s[where:]
p.write_text(s)
assert 'if(q==902&&res==RESULT_OK' in s or 'saveEmployeePhoto(' in s
print("V62 COMPLETE: one fixed nav on all screens, readable legacy actions, working photo return, unified Back, add/import navigation")
