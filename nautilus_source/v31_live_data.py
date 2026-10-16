from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 int[] liveTodayCounts(){
  String day=new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(new Date());int expected=0,present=0,absent=0,late=0;Cursor c=db.getReadableDatabase().rawQuery("SELECT id FROM people WHERE active=1",null);while(c.moveToNext()){DayResult r=calcDay(c.getString(0),day);if(r!=null&&r.expected){expected++;if(r.worked>0){present++;if(r.late>0)late++;}else absent++;}}c.close();return new int[]{expected,present,absent,late};
 }
 void liveStatsRow(){
  int[] n=liveTodayCounts();LinearLayout r=new LinearLayout(this);r.setOrientation(LinearLayout.HORIZONTAL);String[] t={"DEBÍAN TRABAJAR","PRESENTES","AUSENTE","TARDE"};int[] co={Color.rgb(60,105,125),Color.rgb(40,180,115),Color.rgb(210,60,75),Color.rgb(210,160,35)};for(int i=0;i<4;i++){LinearLayout x=exactStat(""+n[i],t[i],co[i]);LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,-2,1);lp.setMargins(3,5,3,5);r.addView(x,lp);}body.addView(r);
 }
 void liveCoverage(){
  sectionTitle("COBERTURA POR SECTOR","Según diagrama y fichadas de hoy");String day=new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(new Date());Cursor sct=db.getReadableDatabase().rawQuery("SELECT name FROM sectors ORDER BY name",null);while(sct.moveToNext()){String sec=sct.getString(0);int exp=0,pre=0;Cursor p=db.getReadableDatabase().rawQuery("SELECT id FROM people WHERE active=1 AND sector=?",new String[]{sec});while(p.moveToNext()){DayResult r=calcDay(p.getString(0),day);if(r!=null&&r.expected){exp++;if(r.worked>0)pre++;}}p.close();int co=pre>=exp&&exp>0?Color.rgb(48,205,166):Color.rgb(235,82,82);LinearLayout row=referenceRow("◈",sec,"",pre+" / "+exp,co);final String fs=sec;row.setOnClickListener(v->liveSector(fs,day));body.addView(row);}sct.close();
 }
 void liveSector(String sec,String day){
  currentScreen="SECTOR";base(sec.toUpperCase());body.addView(refHero(sec.toUpperCase(),"Personal programado · "+day));Cursor p=db.getReadableDatabase().rawQuery("SELECT id,name FROM people WHERE active=1 AND sector=? ORDER BY name",new String[]{sec});while(p.moveToNext()){String id=p.getString(0),name=p.getString(1);DayResult r=calcDay(id,day);if(r==null||!r.expected)continue;String st=r.worked<=0?"NO REGISTRÓ ENTRADA":r.late>0?"LLEGÓ TARDE ("+r.late+" min)":"PRESENTE";int co=r.worked<=0?Color.rgb(235,82,82):r.late>0?Color.rgb(244,190,46):Color.rgb(48,205,166);LinearLayout row=employeeDayCard(id,name,sec,"Turno programado según diagrama",st,co);final String fid=id;row.setOnClickListener(v->exactPersonal(fid));body.addView(row);}p.close();exactBottom("HOY");
 }
'''
s=s.replace(mark,code+"\n"+mark)
s=s.replace('exactStatsRow();exactCoverage();exactBottom("HOY");','liveStatsRow();liveCoverage();exactBottom("HOY");')
s=s.replace('V30 EXACT NAVIGATION','V31 LIVE DATA')
p.write_text(s)
print("V31 live data dashboard applied")
