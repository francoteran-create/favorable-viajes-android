from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 int mtDp(float n){return (int)(n*getResources().getDisplayMetrics().density+.5f);}
 android.graphics.drawable.GradientDrawable mtBg(int top,int bottom,int stroke,int radius){
  android.graphics.drawable.GradientDrawable d=new android.graphics.drawable.GradientDrawable(android.graphics.drawable.GradientDrawable.Orientation.TL_BR,new int[]{top,bottom});
  d.setCornerRadius(mtDp(radius));d.setStroke(mtDp(1),stroke);return d;
 }
 TextView mtText(String txt,int size,int color,boolean bold){
  TextView t=new TextView(this);t.setText(txt);t.setTextSize(size);t.setTextColor(color);t.setGravity(Gravity.CENTER_VERTICAL);
  if(bold)t.setTypeface(android.graphics.Typeface.DEFAULT,android.graphics.Typeface.BOLD);
  t.setIncludeFontPadding(true);return t;
 }
 int mtGold(){return Color.rgb(247,198,97);}
 int mtPale(){return Color.rgb(177,206,225);}
 android.graphics.drawable.Drawable mtLake(final boolean dark){
  return new android.graphics.drawable.Drawable(){
   android.graphics.Paint pt=new android.graphics.Paint(3);
   public void draw(android.graphics.Canvas cv){
    android.graphics.Rect b=getBounds();int save=cv.save();
    cv.translate(b.left,b.top);cv.scale(b.width()/900f,b.height()/310f);
    pt.setShader(new android.graphics.LinearGradient(0,0,0,310,new int[]{Color.rgb(5,17,34),Color.rgb(15,40,67),Color.rgb(116,52,43),Color.rgb(7,33,51),Color.rgb(2,16,34)},new float[]{0f,.25f,.52f,.57f,1f},android.graphics.Shader.TileMode.CLAMP));
    cv.drawRect(0,0,900,310,pt);pt.setShader(null);
    android.graphics.Path hills=new android.graphics.Path();
    hills.moveTo(0,142);hills.lineTo(35,126);hills.lineTo(64,132);hills.lineTo(110,102);hills.lineTo(156,127);hills.lineTo(214,104);hills.lineTo(270,128);hills.lineTo(337,97);hills.lineTo(389,126);hills.lineTo(452,107);hills.lineTo(498,126);hills.lineTo(562,94);hills.lineTo(618,123);hills.lineTo(670,115);hills.lineTo(740,134);hills.lineTo(900,114);hills.lineTo(900,180);hills.lineTo(0,180);hills.close();
    pt.setColor(Color.rgb(3,17,31));cv.drawPath(hills,pt);
    pt.setShader(new android.graphics.LinearGradient(0,155,0,310,Color.rgb(11,56,75),Color.rgb(2,11,27),android.graphics.Shader.TileMode.CLAMP));
    cv.drawRect(0,156,900,310,pt);pt.setShader(null);
    // Distant marina silhouettes and warm windows.
    pt.setColor(Color.rgb(4,13,22));cv.drawRect(0,143,180,170,pt);cv.drawRect(715,104,900,179,pt);
    cv.drawRect(760,78,880,112,pt);cv.drawRect(785,60,885,76,pt);
    for(int x=772;x<890;x+=23){pt.setColor(Color.rgb(252,183,69));cv.drawRect(x,118,x+10,150,pt);pt.setColor(Color.rgb(18,38,55));cv.drawRect(x+2,119,x+7,150,pt);}
    pt.setColor(Color.rgb(3,10,21));android.graphics.Path pier=new android.graphics.Path();pier.moveTo(880,176);pier.lineTo(650,170);pier.lineTo(535,265);pier.lineTo(865,215);pier.close();cv.drawPath(pier,pt);
    for(int i=0;i<33;i++){float x=(i*137+23)%880+7;float y=165+(i%4)*4;pt.setColor(Color.argb(100,250,174,63));cv.drawCircle(x,y,5,pt);pt.setColor(Color.rgb(255,206,99));cv.drawCircle(x,y,1.7f,pt);}
    for(int i=0;i<38;i++){float x=(i*137+23)%880+7;float y=185+(i%3)*6;pt.setColor(Color.argb(32+(i%5)*9,255,184,83));cv.drawRect(x,y,x+2,Math.min(305,y+14+(i*9)%57),pt);}
    for(int i=0;i<48;i++){float y=182+i*2.4f;float x=90+(i*71)%700;pt.setColor(Color.argb(16,108,193,222));cv.drawRect(x,y,x+30+(i%4)*13,y+1,pt);}
    if(dark){pt.setColor(Color.argb(95,0,7,18));cv.drawRect(0,0,900,310,pt);}
    cv.restoreToCount(save);
   }
   public void setAlpha(int a){} public void setColorFilter(android.graphics.ColorFilter f){}
   public int getOpacity(){return android.graphics.PixelFormat.TRANSLUCENT;}
  };
 }
 LinearLayout mtNavigation(int selected){
  LinearLayout nav=new LinearLayout(this);nav.setOrientation(LinearLayout.HORIZONTAL);nav.setBackgroundColor(Color.rgb(2,13,26));nav.setPadding(mtDp(3),mtDp(2),mtDp(3),mtDp(2));
  String[] icons={"⌂","▣","●","▥","⚙"};String[] labs={"INICIO","TURNOS","PERSONAL","INFORMES","CONFIG."};
  Runnable[] actions={this::masterImageHomeV59,()->mtWeek(new Date()),this::mtPersonnel,this::mtReports,this::mtConfig};
  for(int i=0;i<5;i++){
   LinearLayout cell=new LinearLayout(this);cell.setOrientation(LinearLayout.VERTICAL);cell.setGravity(Gravity.CENTER);cell.setPadding(0,mtDp(4),0,0);
   TextView icon=mtText(icons[i],20,i==selected?mtGold():Color.rgb(208,225,235),true);icon.setGravity(Gravity.CENTER);
   TextView label=mtText(labs[i],9,i==selected?mtGold():Color.rgb(213,224,235),true);label.setGravity(Gravity.CENTER);label.setSingleLine(true);
   cell.addView(icon,new LinearLayout.LayoutParams(-1,mtDp(29)));cell.addView(label,new LinearLayout.LayoutParams(-1,mtDp(20)));
   final int idx=i;cell.setContentDescription(labs[i]);cell.setOnClickListener(v->actions[idx].run());
   if(i==selected)cell.setBackground(mtBg(Color.rgb(30,37,37),Color.rgb(3,19,33),Color.rgb(107,85,47),12));
   nav.addView(cell,new LinearLayout.LayoutParams(0,-1,1));
  }
  return nav;
 }
 void mtScreen(String title,int selected){
  LinearLayout root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setBackgroundResource(R.drawable.nautilus_home_bg);
  ScrollView scroll=new ScrollView(this);scroll.setFillViewport(true);scroll.setVerticalScrollBarEnabled(false);
  body=new LinearLayout(this);body.setOrientation(LinearLayout.VERTICAL);body.setPadding(mtDp(10),mtDp(8),mtDp(10),mtDp(13));
  scroll.addView(body,new ScrollView.LayoutParams(-1,-2));root.addView(scroll,new LinearLayout.LayoutParams(-1,0,1));
  root.addView(mtNavigation(selected),new LinearLayout.LayoutParams(-1,mtDp(62)));setContentView(root);
  if(title!=null&&!title.isEmpty()){
   TextView heading=mtText(title,22,mtGold(),true);heading.setPadding(mtDp(10),mtDp(8),0,mtDp(10));body.addView(heading);
  }
 }
 void mtHeader(){
  FrameLayout head=new FrameLayout(this);head.setBackground(mtLake(false));
  ImageView emblem=new ImageView(this);emblem.setImageResource(R.drawable.nautilus_logo_futuristic);emblem.setScaleType(ImageView.ScaleType.FIT_CENTER);
  android.graphics.drawable.GradientDrawable ring=mtBg(Color.rgb(2,21,41),Color.rgb(2,13,28),mtGold(),80);emblem.setBackground(ring);
  FrameLayout.LayoutParams el=new FrameLayout.LayoutParams(mtDp(112),mtDp(112),Gravity.CENTER_HORIZONTAL|Gravity.TOP);el.topMargin=mtDp(4);head.addView(emblem,el);emblem.setOnClickListener(v->masterImageHomeV59());
  TextView name=mtText("NAUTILUS",16,mtGold(),true);name.setGravity(Gravity.CENTER);name.setLetterSpacing(.16f);
  FrameLayout.LayoutParams np=new FrameLayout.LayoutParams(-1,mtDp(23),Gravity.BOTTOM);np.bottomMargin=mtDp(17);head.addView(name,np);
  TextView country=mtText("COUNTRY NÁUTICO  ·  PRESENTISMO",9,Color.WHITE,true);country.setGravity(Gravity.CENTER);country.setLetterSpacing(.1f);
  FrameLayout.LayoutParams cp=new FrameLayout.LayoutParams(-1,mtDp(16),Gravity.BOTTOM);cp.bottomMargin=mtDp(2);head.addView(country,cp);
  TextView menu=mtText("☰",25,Color.WHITE,true);menu.setGravity(Gravity.CENTER);menu.setBackground(mtBg(0xBB071C30,0xE803101E,0xAA659BB7,15));FrameLayout.LayoutParams mp=new FrameLayout.LayoutParams(mtDp(48),mtDp(48),Gravity.LEFT|Gravity.TOP);mp.leftMargin=mtDp(9);mp.topMargin=mtDp(13);head.addView(menu,mp);menu.setOnClickListener(v->mtConfig());
  TextView bell=mtText("♟",23,Color.WHITE,true);bell.setGravity(Gravity.CENTER);bell.setText("●");bell.setBackground(mtBg(0xBB071C30,0xE803101E,0xAA659BB7,15));FrameLayout.LayoutParams bp=new FrameLayout.LayoutParams(mtDp(48),mtDp(48),Gravity.RIGHT|Gravity.TOP);bp.rightMargin=mtDp(9);bp.topMargin=mtDp(13);head.addView(bell,bp);bell.setOnClickListener(v->reviews());bell.setContentDescription("Avisos e incidencias");
  LinearLayout.LayoutParams hp=new LinearLayout.LayoutParams(-1,mtDp(176));hp.bottomMargin=mtDp(8);body.addView(head,hp);
 }
 LinearLayout mtFeature(String glyph,String heading,String sub,Runnable click,boolean major){
  LinearLayout card=new LinearLayout(this);card.setOrientation(LinearLayout.HORIZONTAL);card.setGravity(Gravity.CENTER_VERTICAL);
  card.setPadding(mtDp(12),mtDp(8),mtDp(10),mtDp(8));
  card.setBackground(major?mtLake(true):mtBg(0xF8092940,0xF9030F21,Color.rgb(48,111,149),18));
  TextView pict=mtText(glyph,major?34:30,mtGold(),true);pict.setGravity(Gravity.CENTER);card.addView(pict,new LinearLayout.LayoutParams(mtDp(49),-1));
  LinearLayout stack=new LinearLayout(this);stack.setGravity(Gravity.CENTER_VERTICAL);stack.setOrientation(LinearLayout.VERTICAL);
  TextView title=mtText(heading,major?22:14,Color.WHITE,true);title.setMaxLines(2);title.setEllipsize(null);
  TextView subtitle=mtText(sub,major?12:11,mtPale(),false);subtitle.setMaxLines(2);
  stack.addView(title,new LinearLayout.LayoutParams(-1,-2));stack.addView(subtitle,new LinearLayout.LayoutParams(-1,-2));
  card.addView(stack,new LinearLayout.LayoutParams(0,-1,1));
  TextView arr=mtText("›",major?34:27,mtGold(),false);arr.setGravity(Gravity.CENTER);card.addView(arr,new LinearLayout.LayoutParams(mtDp(20),-1));
  card.setContentDescription(heading+": "+sub);card.setOnClickListener(v->click.run());card.setMinimumHeight(mtDp(major?84:86));return card;
 }
 LinearLayout mtPanel(){
  LinearLayout x=new LinearLayout(this);x.setOrientation(LinearLayout.VERTICAL);x.setPadding(mtDp(9),mtDp(10),mtDp(9),mtDp(12));
  x.setBackground(mtBg(0xF5092538,0xFF03101E,Color.rgb(46,100,138),20));return x;
 }
 LinearLayout mtPanelTitle(String title,String right,Runnable action){
  LinearLayout r=new LinearLayout(this);r.setOrientation(LinearLayout.HORIZONTAL);r.setGravity(Gravity.CENTER_VERTICAL);
  TextView a=mtText(title,15,Color.WHITE,true);r.addView(a,new LinearLayout.LayoutParams(0,mtDp(32),1));
  TextView b=mtText(right,10,mtPale(),true);b.setGravity(Gravity.CENTER);
  b.setBackground(mtBg(0x66172C40,0x66020E1A,Color.rgb(67,138,184),18));b.setPadding(mtDp(9),0,mtDp(9),0);
  if(action!=null)b.setOnClickListener(v->action.run());r.addView(b,new LinearLayout.LayoutParams(-2,mtDp(30)));return r;
 }
 LinearLayout mtStat(String value,String label,int accent){
  LinearLayout x=new LinearLayout(this);x.setOrientation(LinearLayout.VERTICAL);x.setGravity(Gravity.CENTER);
  x.setBackground(mtBg(0xF50B2939,0xFF020C18,accent,14));x.setPadding(mtDp(1),mtDp(5),mtDp(1),mtDp(5));
  TextView n=mtText(value,23,accent,true);n.setGravity(Gravity.CENTER);TextView t=mtText(label,9,Color.rgb(222,232,237),false);t.setGravity(Gravity.CENTER);t.setMaxLines(2);
  x.addView(n,new LinearLayout.LayoutParams(-1,mtDp(34)));x.addView(t,new LinearLayout.LayoutParams(-1,mtDp(30)));return x;
 }
 int mtLicenses(){
  int n=0;try{
   String ym=new SimpleDateFormat("yyyy-MM",Locale.US).format(new Date())+"%";
   Cursor c=db.getReadableDatabase().rawQuery("SELECT COUNT(*) FROM overrides WHERE UPPER(kind) LIKE '%LICEN%' AND work_date LIKE ?",new String[]{ym});
   if(c.moveToFirst())n=c.getInt(0);c.close();
  }catch(Exception ignored){}return n;
 }
 void mtSummary(){
  LinearLayout p=mtPanel();p.addView(mtPanelTitle("RESUMEN DEL MES","VER DETALLE  ›",()->quickReport(true)));
  int[] st=homeMonthStats();String[] n={""+st[1],""+st[3],""+st[2],""+mtLicenses()};
  String[] labs={"Asistencias","Ausencias","Tardanzas","Licencias"};
  int[] col={Color.rgb(58,227,121),Color.rgb(251,86,95),mtGold(),Color.rgb(84,178,249)};
  LinearLayout row=new LinearLayout(this);row.setOrientation(LinearLayout.HORIZONTAL);
  for(int i=0;i<4;i++){LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,mtDp(79),1);lp.setMargins(mtDp(2),mtDp(5),mtDp(2),0);row.addView(mtStat(n[i],labs[i],col[i]),lp);}p.addView(row);
  LinearLayout.LayoutParams pp=new LinearLayout.LayoutParams(-1,-2);pp.topMargin=mtDp(12);body.addView(p,pp);
 }
 void mtWeekStrip(){
  LinearLayout p=mtPanel();p.addView(mtPanelTitle("SEMANA ACTUAL","VER SEMANA  ›",()->mtWeek(new Date())));
  Calendar mon=mondayOf(new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(new Date()));Calendar today=Calendar.getInstance();
  String isToday=new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(today.getTime());
  String[] week={"LUN","MAR","MIÉ","JUE","VIE","SÁB","DOM"};
  LinearLayout row=new LinearLayout(this);row.setOrientation(LinearLayout.HORIZONTAL);
  for(int i=0;i<7;i++){
   String date=isoDay(mon);boolean chosen=date.equals(isToday);
   LinearLayout day=new LinearLayout(this);day.setOrientation(LinearLayout.VERTICAL);day.setGravity(Gravity.CENTER);
   day.setBackground(mtBg(chosen?0xFF06385A:0xFF082439,0xFF031321,chosen?0xFF1DBDFF:0xFF205778,13));
   TextView dn=mtText(week[i],10,Color.WHITE,true);dn.setGravity(Gravity.CENTER);
   TextView num=mtText(String.format(Locale.US,"%02d",mon.get(Calendar.DAY_OF_MONTH)),19,Color.WHITE,true);num.setGravity(Gravity.CENTER);
   day.addView(dn,new LinearLayout.LayoutParams(-1,mtDp(23)));day.addView(num,new LinearLayout.LayoutParams(-1,mtDp(28)));
   TextView hint=mtText(chosen?"HOY":"•",9,chosen?mtGold():mtPale(),true);hint.setGravity(Gravity.CENTER);day.addView(hint,new LinearLayout.LayoutParams(-1,mtDp(17)));
   final String ds=date;day.setOnClickListener(v->exactDayRoster(ds));day.setContentDescription(date+" · ver personal diagramado");
   LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,mtDp(76),1);lp.setMargins(mtDp(2),mtDp(8),mtDp(2),0);row.addView(day,lp);
   mon.add(Calendar.DAY_OF_MONTH,1);
  }
  p.addView(row);LinearLayout.LayoutParams pp=new LinearLayout.LayoutParams(-1,-2);pp.topMargin=mtDp(11);body.addView(p,pp);
 }
 void masterImageHomeV59(){
  currentScreen="INICIO";mtScreen("",0);mtHeader();
  LinearLayout hero=mtFeature("▦","TURNOS","Personal y diagramación",()->mtWeek(new Date()),true);
  LinearLayout.LayoutParams h=new LinearLayout.LayoutParams(-1,mtDp(91));h.bottomMargin=mtDp(7);body.addView(hero,h);
  LinearLayout row=new LinearLayout(this);row.setOrientation(LinearLayout.HORIZONTAL);
  LinearLayout.LayoutParams a=new LinearLayout.LayoutParams(0,mtDp(100),1);a.rightMargin=mtDp(4);row.addView(mtFeature("♟","PERSONAL","Fichas y estadísticas",this::mtPersonnel,false),a);
  LinearLayout.LayoutParams b=new LinearLayout.LayoutParams(0,mtDp(100),1);b.leftMargin=mtDp(4);row.addView(mtFeature("▥","INFORMES","Reportes y exportación",this::mtReports,false),b);
  body.addView(row);
  LinearLayout row2=new LinearLayout(this);row2.setOrientation(LinearLayout.HORIZONTAL);
  LinearLayout.LayoutParams c=new LinearLayout.LayoutParams(0,mtDp(100),1);c.rightMargin=mtDp(4);row2.addView(mtFeature("⚙","CONFIGURACIÓN","Sectores y horarios",this::mtConfig,false),c);
  LinearLayout.LayoutParams d=new LinearLayout.LayoutParams(0,mtDp(100),1);d.leftMargin=mtDp(4);row2.addView(mtFeature("⇩","IMPORTAR FICHADAS","Reloj biométrico",()->attendance(new Date()),false),d);
  LinearLayout.LayoutParams r2=new LinearLayout.LayoutParams(-1,-2);r2.topMargin=mtDp(7);body.addView(row2,r2);
  mtSummary();mtWeekStrip();
 }
 void mtAddLink(String symbol,String title,String caption,Runnable action){
  LinearLayout x=mtFeature(symbol,title,caption,action,false);LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,mtDp(88));lp.bottomMargin=mtDp(8);body.addView(x,lp);
 }
 void mtWeek(Date focus){
  currentScreen="SEMANA";mtScreen("TURNOS · SEMANA",1);
  Calendar start=Calendar.getInstance();start.setTime(focus);int dow=start.get(Calendar.DAY_OF_WEEK);start.add(Calendar.DAY_OF_MONTH,-((dow+5)%7));
  Calendar end=(Calendar)start.clone();end.add(Calendar.DAY_OF_MONTH,6);
  TextView period=mtText(new SimpleDateFormat("dd/MM",Locale.US).format(start.getTime())+" — "+new SimpleDateFormat("dd/MM/yyyy",Locale.US).format(end.getTime()),15,mtPale(),true);body.addView(period);
  LinearLayout controls=new LinearLayout(this);controls.setOrientation(LinearLayout.HORIZONTAL);controls.setGravity(Gravity.CENTER);
  String[] a={"‹ ANTERIOR","HOY","SIGUIENTE ›"};
  for(int i=0;i<3;i++){final int k=i;TextView t=mtText(a[i],12,mtGold(),true);t.setGravity(Gravity.CENTER);t.setBackground(mtBg(0xFF0D2B3A,0xFF051522,Color.rgb(45,121,166),12));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,mtDp(48),1);lp.setMargins(mtDp(3),mtDp(10),mtDp(3),mtDp(12));controls.addView(t,lp);t.setOnClickListener(v->{Calendar n=Calendar.getInstance();n.setTime(focus);if(k==0)n.add(Calendar.DAY_OF_MONTH,-7);if(k==2)n.add(Calendar.DAY_OF_MONTH,7);mtWeek(k==1?new Date():n.getTime());});}body.addView(controls);
  for(int i=0;i<7;i++){
   final String ds=isoDay(start);
   String dayName=new SimpleDateFormat("EEEE dd/MM",new Locale("es","AR")).format(start.getTime()).toUpperCase(new Locale("es","AR"));
   int scheduled=0;try{Cursor cur=db.getReadableDatabase().rawQuery("SELECT id FROM people WHERE active=1",null);while(cur.moveToNext()){DayResult x=calcDay(cur.getString(0),ds);if(x!=null&&x.expected)scheduled++;}cur.close();}catch(Exception ignored){}
   String state=evaluatedThrough(ds)==0?"Programado · fichadas pendientes de importar":"Fichadas importadas";
   mtAddLink("▣",dayName,scheduled+" personas diagramadas · "+state,()->exactDayRoster(ds));start.add(Calendar.DAY_OF_MONTH,1);
  }
 }
 void mtPersonnel(){
  currentScreen="PERSONAL";mtScreen("PERSONAL",2);
  mtAddLink("+","AGREGAR PERSONAL","Alta manual y configuración de empleado",()->editPerson(null));
  int count=0;Cursor c=null;
  try{c=db.getReadableDatabase().rawQuery("SELECT p.id,p.name,coalesce(s.name,'SIN SECTOR') FROM people p LEFT JOIN sectors s ON s.id=p.sector_id WHERE p.active=1 ORDER BY p.name",null);
   while(c.moveToNext()){String id=c.getString(0),name=c.getString(1),sector=c.getString(2);count++;mtAddLink("●",name,sector+" · ficha, foto y diagramación",()->exactPersonal(id));}
  }catch(Exception e){body.addView(mtText("Error al cargar personal: "+e.getMessage(),13,mtPale(),false));}finally{if(c!=null)c.close();}
  if(count==0)body.addView(mtText("Todavía no hay personal cargado. Tocá AGREGAR PERSONAL o importá las fichadas para identificar empleados.",13,mtPale(),false));
 }
 void mtReports(){
  currentScreen="INFORMES";mtScreen("INFORMES",3);
  mtAddLink("▣","INFORME SEMANAL","Personal, asistencias e incidencias · lunes a domingo",()->quickReport(false));
  mtAddLink("▥","INFORME MENSUAL","Período mensual y resumen por persona",()->quickReport(true));
  mtAddLink("▤","ESTADÍSTICAS","Control por empleado y sector",this::managementSummary);
  mtAddLink("⇩","EXPORTAR CSV / EXCEL","Guardar informe de presentismo",this::exportCsv);
  mtAddLink("◧","DOCUMENTO PDF","Preparar informe imprimible",this::reports);
 }
 void mtConfig(){
  currentScreen="CONFIG";mtScreen("CONFIGURACIÓN",4);
  mtAddLink("⇩","IMPORTAR FICHADAS","Archivo descargado del reloj biométrico",()->attendance(new Date()));
  mtAddLink("●","GESTIONAR PERSONAL","Altas, fichas y fotografías",this::mtPersonnel);
  mtAddLink("⚙","SECTORES Y REGÍMENES","Horarios, tolerancias y ciclos de turnos",this::exactMoreLive);
  mtAddLink("▣","DIAGRAMACIÓN","Semana y turnos planificados",()->mtWeek(new Date()));
  mtAddLink("▥","INFORMES","Estadísticas, PDF, Excel",this::mtReports);
 }
'''
s=s.replace(mark,code+"\n"+mark,1)
# Consolidate the initial launcher and legacy Home/back targets without touching the financial/attendance logic.
s=s.replace("this::masterImageHomeV58","this::masterImageHomeV59")
s=s.replace("masterImageHomeV58();","masterImageHomeV59();")
# Old safe-boot code is not invoked.
p.write_text(s)
print("V59: cinematic scenic Nautilus home; real independent labels; responsive cards; live stats/week; shared functional menus")
