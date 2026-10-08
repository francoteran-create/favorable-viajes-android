from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 void operationBanner(int expected,int present,int absent,int late){
  boolean ok=absent==0&&late==0;int col=ok?Color.rgb(48,205,166):Color.rgb(244,190,46);
  body.addView(premiumCard(ok?"OPERACIÓN NORMAL":"REQUIERE ATENCIÓN",ok?"✓ COBERTURA CONTROLADA":"⚠ HAY NOVEDADES",ok?"Todo el personal esperado está cubierto":(absent+" ausente(s) · "+late+" tardanza(s)"),col));
 }
 int[] sectorCoverageToday(String sector){
  int exp=0,pre=0;String day=new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(new Date());
  Cursor c=db.getReadableDatabase().rawQuery("SELECT p.id FROM people p LEFT JOIN sectors s ON s.id=p.sector_id WHERE p.active=1 AND s.name=?",new String[]{sector});
  while(c.moveToNext()){DayResult r=calcDay(c.getString(0),day);if(r!=null&&r.expected){exp++;if(r.worked>0)pre++;}}c.close();return new int[]{pre,exp};
 }
 void coverageReferenceLive(){
  sectionTitle("COBERTURA POR SECTOR","Dotación prevista y presente");
  Cursor c=db.getReadableDatabase().rawQuery("SELECT name FROM sectors ORDER BY name",null);
  while(c.moveToNext()){final String sec=c.getString(0);int[] z=sectorCoverageToday(sec);boolean ok=z[1]==0||z[0]>=z[1];int col=ok?Color.rgb(48,205,166):Color.rgb(235,82,82);addRefRow(ok?"✓":"! ",sec,z[1]==0?"Sin dotación prevista":"Cobertura del turno",z[0]+"/"+z[1],col,()->sectorDetail(sec));}c.close();
 }
'''
s=s.replace(mark,code+"\n"+mark)
# In dashboard place operational banner before metrics if the known metrics injection exists.
needle='operationalStats(totalExpected,totalPresent,totalAbsent,totalLate);coverageReference();'
if needle in s:s=s.replace(needle,'operationBanner(totalExpected,totalPresent,totalAbsent,totalLate);operationalStats(totalExpected,totalPresent,totalAbsent,totalLate);coverageReferenceLive();')
# Worker rows: expose today's first/last punch times from immutable punches.
needle2='String nm=c.getString(1),reg=c.getString(2);DayResult dr=calcDay(id,day);'
if needle2 in s:
 s=s.replace(needle2,'''String nm=c.getString(1),reg=c.getString(2);DayResult dr=calcDay(id,day);String punch="Sin fichada";Cursor pc=db.getReadableDatabase().rawQuery("SELECT MIN(ts),MAX(ts) FROM punches WHERE person_id=? AND substr(ts,1,10)=?",new String[]{id,day});if(pc.moveToFirst()&&pc.getString(0)!=null){String a=pc.getString(0),b=pc.getString(1);punch=(a.length()>=16?a.substring(11,16):a)+(a.equals(b)?"":" → "+(b.length()>=16?b.substring(11,16):b));}pc.close();''')
 old='addRefRow("●",nm,reg+" · "+state,"›",col,()->employeeProfile(id));'
 new='addRefRow("●",nm,punch+" · "+reg+" · "+state,"›",col,()->employeeProfile(id));'
 s=s.replace(old,new)
# Reference title date and version marker.
s=s.replace('V16 NUCLEAR','V17 REACTOR')
p.write_text(s)
print("V17 reactor operational fidelity applied")
