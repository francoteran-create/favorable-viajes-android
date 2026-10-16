from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
def replace_method(name,body):
 global s
 match=re.search(r'\bvoid\s+'+re.escape(name)+r'\s*\([^)]*\)\s*\{',s)
 assert match,name
 first=s.index('{',match.start());level=0;quote=None;escape=False
 for pos in range(first,len(s)):
  ch=s[pos]
  if quote:
   if escape:escape=False
   elif ch=='\\':escape=True
   elif ch==quote:quote=None
   continue
  if ch in ('"',"'"):quote=ch;continue
  if ch=='{':level+=1
  if ch=='}':
   level-=1
   if level==0:
    s=s[:match.start()]+body+s[pos+1:];return
 raise RuntimeError(name)
add=r'''
 String hmChosenKey(){
  String stored=getSharedPreferences("nautilus_home",MODE_PRIVATE).getString("summary_month",null);
  if(stored!=null&&stored.matches("\\d{4}-\\d\\d"))return stored;
  return new SimpleDateFormat("yyyy-MM",Locale.US).format(new Date());
 }
 void hmChooseMonth(int year){
  currentScreen="MESES";mtScreen("ELEGIR MES DEL RESUMEN",0);
  body.addView(mtText("Al elegir un mes, volverás al inicio y se actualizarán las cuatro tarjetas de colores.",13,mtPale(),false));
  LinearLayout bar=new LinearLayout(this);bar.setOrientation(LinearLayout.HORIZONTAL);
  TextView back=mtText("‹ AÑO",17,mtGold(),true);back.setGravity(Gravity.CENTER);back.setOnClickListener(v->hmChooseMonth(year-1));
  TextView middle=mtText(""+year,22,Color.WHITE,true);middle.setGravity(Gravity.CENTER);
  TextView forward=mtText("AÑO ›",17,mtGold(),true);forward.setGravity(Gravity.CENTER);forward.setOnClickListener(v->hmChooseMonth(year+1));
  bar.addView(back,new LinearLayout.LayoutParams(0,mtDp(58),1));bar.addView(middle,new LinearLayout.LayoutParams(0,mtDp(58),1));
  bar.addView(forward,new LinearLayout.LayoutParams(0,mtDp(58),1));body.addView(bar);
  String[] months={"ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"};
  for(int m=0;m<12;m++){
   final String ym=String.format(Locale.US,"%04d-%02d",year,m+1);
   Cursor cc=db.getReadableDatabase().rawQuery("SELECT COUNT(*),COUNT(DISTINCT person_id),COUNT(DISTINCT person_id || '|' || substr(stamp,1,10)) FROM punches WHERE substr(stamp,1,7)=?",new String[]{ym});
   int marks=0,persons=0,attendDays=0;
   try{if(cc.moveToFirst()){marks=cc.getInt(0);persons=cc.getInt(1);attendDays=cc.getInt(2);}}finally{cc.close();}
   String desc=marks+" fichadas · "+persons+" personas · "+attendDays+" asistencias registradas";
   mtAddLink("▦",months[m]+" "+year,desc,()->{
    getSharedPreferences("nautilus_home",MODE_PRIVATE).edit().putString("summary_month",ym).apply();
    masterImageHomeV59();
   });
  }
 }
 void hmChooseMonth(){String ym=hmChosenKey();hmChooseMonth(Integer.parseInt(ym.substring(0,4)));}
 int[] hmSummaryCounts(String ym){
  int[] totals=new int[4];
  SQLiteDatabase r=db.getReadableDatabase();
  Cursor attendance=r.rawQuery("SELECT COUNT(*) FROM (SELECT person_id,substr(stamp,1,10) AS day FROM punches WHERE substr(stamp,1,7)=? GROUP BY person_id,day)",new String[]{ym});
  try{if(attendance.moveToFirst())totals[0]=attendance.getInt(0);}finally{attendance.close();}
  // Licence/absence counts are based on explicit statuses, not missing punch data alone.
  Cursor leaves=r.rawQuery("SELECT COUNT(*) FROM overrides WHERE substr(work_date,1,7)=? AND UPPER(kind) LIKE '%LICEN%'",new String[]{ym});
  try{if(leaves.moveToFirst())totals[3]=leaves.getInt(0);}finally{leaves.close();}
  try{
   Cursor absence=r.rawQuery("SELECT COUNT(*) FROM reviews WHERE substr(work_date,1,7)=? AND (UPPER(status) LIKE '%AUSEN%' OR UPPER(status) LIKE '%FALTA%')",new String[]{ym});
   try{if(absence.moveToFirst())totals[1]=absence.getInt(0);}finally{absence.close();}
  }catch(Exception ignored){}
  try{
   rsEnsure();
   Cursor late=r.rawQuery(
    "SELECT s.person_id,s.work_date,s.start_time,MIN(substr(p.stamp,12,5)) "+
    "FROM scheduled_shifts s JOIN punches p ON p.person_id=s.person_id AND substr(p.stamp,1,10)=s.work_date "+
    "WHERE substr(s.work_date,1,7)=? AND s.start_time!='FRANCO' GROUP BY s.person_id,s.work_date,s.start_time",
    new String[]{ym});
   try{while(late.moveToNext()){
    String id=late.getString(0),plan=late.getString(2),first=late.getString(3);
    int scheduled=rsMinutes(plan),actual=rsMinutes(first);
    String[] rule=hrRule(id);int grace=10;
    try{grace=Integer.parseInt(rule[2]);}catch(Exception ignored){}
    if(scheduled>=0&&actual>scheduled+grace)totals[2]++;
   }}finally{late.close();}
  }catch(Exception ignored){}
  return totals;
 }
 void hmReportButtons(String from,String to,String pid){
  LinearLayout row=new LinearLayout(this);row.setOrientation(LinearLayout.HORIZONTAL);
  TextView save=mtText("▧ GUARDAR PDF",12,mtGold(),true);
  TextView open=mtText("◷ ABRIR / BUSCAR",12,Color.WHITE,true);
  save.setGravity(Gravity.CENTER);open.setGravity(Gravity.CENTER);
  save.setBackground(mtBg(0xFF153A4F,0xFF071725,0xFF5EA0BD,12));
  open.setBackground(mtBg(0xFF153A4F,0xFF071725,0xFF5EA0BD,12));
  save.setOnClickListener(v->hrSavePdf(from,to,pid));
  open.setOnClickListener(v->hrBrowseReport());
  LinearLayout.LayoutParams a=new LinearLayout.LayoutParams(0,mtDp(54),1);a.rightMargin=mtDp(4);
  LinearLayout.LayoutParams b=new LinearLayout.LayoutParams(0,mtDp(54),1);b.leftMargin=mtDp(4);
  row.addView(save,a);row.addView(open,b);body.addView(row);
  body.addView(mtText("ABRIR / BUSCAR abre el selector de Android para localizar el informe en la carpeta donde lo guardaste.",11,mtPale(),false));
 }
'''
assert ' void dualClockHub(){' in s
s=s.replace(' void dualClockHub(){',add+'\n void dualClockHub(){',1)
summary=r'''void mtSummary(){
  String ym=hmChosenKey();
  String[] months={"ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"};
  int mi=Integer.parseInt(ym.substring(5,7))-1;
  LinearLayout panel=mtPanel();
  panel.addView(mtPanelTitle("RESUMEN DEL MES · "+months[mi]+" "+ym.substring(0,4),"CAMBIAR MES  ›",this::hmChooseMonth));
  int[] st=hmSummaryCounts(ym);
  String[] values={""+st[0],""+st[1],""+st[2],""+st[3]};
  String[] labels={"Asistencias*","Ausencias","Tardanzas","Licencias"};
  int[] colors={Color.rgb(58,227,121),Color.rgb(251,86,95),mtGold(),Color.rgb(84,178,249)};
  LinearLayout strip=new LinearLayout(this);strip.setOrientation(LinearLayout.HORIZONTAL);
  for(int i=0;i<4;i++){
   LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,mtDp(79),1);
   lp.setMargins(mtDp(2),mtDp(5),mtDp(2),0);
   strip.addView(mtStat(values[i],labels[i],colors[i]),lp);
  }
  panel.addView(strip);
  panel.addView(mtText("*Asistencias: días por empleado con fichadas. Ausencias: registros confirmados. Tardanzas: fichadas comparadas con turnos y tolerancia configurados; sin turnos, no se pueden evaluar.",10,mtPale(),false));
  final Calendar focus=Calendar.getInstance();focus.set(Integer.parseInt(ym.substring(0,4)),mi,1);
  mtHomeMonthActions(panel,focus.getTime());
  LinearLayout.LayoutParams pp=new LinearLayout.LayoutParams(-1,-2);
  pp.topMargin=mtDp(12);body.addView(panel,pp);
 }
 void mtHomeMonthActions(LinearLayout panel,Date date){
  TextView details=mtText("VER INFORME DEL MES  ›",12,mtGold(),true);
  details.setGravity(Gravity.CENTER);details.setOnClickListener(v->rpPeriod(date,true));
  panel.addView(details,new LinearLayout.LayoutParams(-1,mtDp(40)));
 }
'''
replace_method('mtSummary',summary)
# Pair save and browse directly where reports are shown. No false claim of direct OS folder opening.
needle='''  mtAddLink("▧","PDF DE HORAS COMUNES Y RECARGO","Membrete y tablas por trabajador",()->hrSavePdf(f,t,null));'''
assert needle in s
s=s.replace(needle,needle+'\n  hmReportButtons(f,t,null);',1)
needle='''  mtAddLink("▧","PDF INDIVIDUAL CON MEMBRETE","Horas comunes y recargo, sin importes",()->hrSavePdf(from,to,pid));'''
assert needle in s
s=s.replace(needle,needle+'\n  hmReportButtons(from,to,pid);',1)
needle='''  mtAddLink("▧","GENERAR PDF CON MEMBRETE","Elegí dónde guardar el documento",()->hrSavePdf(from,to,null));'''
assert needle in s
s=s.replace(needle,needle+'\n  hmReportButtons(from,to,null);',1)
p.write_text(s)
print("V78 home in-place month summary with true attendance days and colored metrics, paired save/browse report controls")
