from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
insert=' void dualClockHub(){'
assert insert in s
code=r'''
 static final int HR_SAVE_PDF=931,HR_PICK_REPORT=932;
 byte[] hrPendingPdf=null;
 void hrEnsure(){
  db.getWritableDatabase().execSQL("CREATE TABLE IF NOT EXISTS hour_rules(person_id TEXT PRIMARY KEY,starts TEXT NOT NULL,ends TEXT NOT NULL)");
 }
 String[] hrRule(String pid){
  hrEnsure();
  Cursor c=db.getReadableDatabase().rawQuery("SELECT starts,ends FROM hour_rules WHERE person_id IN (?, '*') ORDER BY CASE WHEN person_id=? THEN 0 ELSE 1 END LIMIT 1",new String[]{pid,pid});
  String[] rule={"08:00","16:00"};
  try{if(c.moveToFirst()){rule[0]=c.getString(0);rule[1]=c.getString(1);}}finally{c.close();}
  return rule;
 }
 void hrSetRule(String pid,String title){
  hrEnsure();currentScreen="INFORMES";mtScreen("CONFIGURAR HORARIO COMÚN",3);
  String[] existing=hrRule(pid);
  body.addView(mtText(title,19,Color.WHITE,true));
  body.addView(mtText("Las horas dentro del horario serán COMUNES y las restantes se informarán como RECARGO. No se calculan importes. Esta regla no modifica las fichadas ni los turnos.",13,mtPale(),false));
  EditText from=rsInput("COMIENZO DEL HORARIO COMÚN (HH:MM)",existing[0]);
  EditText to=rsInput("FIN DEL HORARIO COMÚN (HH:MM)",existing[1]);
  mtAddLink("✓","GUARDAR HORARIO COMÚN","Aplicar a los próximos informes",()->{
   String start=from.getText().toString().trim(),end=to.getText().toString().trim();
   if(rsMinutes(start)<0||rsMinutes(end)<0||start.equals(end)){
    msg("Horario inválido","Ingresá dos horas HH:MM distintas.",()->hrSetRule(pid,title));return;
   }
   ContentValues v=new ContentValues();v.put("person_id",pid);v.put("starts",start);v.put("ends",end);
   db.getWritableDatabase().insertWithOnConflict("hour_rules",null,v,SQLiteDatabase.CONFLICT_REPLACE);
   msg("Horario guardado",title+" · Horario común: "+start+" a "+end+". Las horas fuera de esta franja se reportarán como recargo, sujetas a revisión.",this::mtReports);
  });
 }
 void hrPersonRulePicker(){
  currentScreen="INFORMES";mtScreen("HORARIO POR EMPLEADO",3);
  Cursor c=db.getReadableDatabase().rawQuery("SELECT id,COALESCE(NULLIF(name,''),id) FROM people WHERE active=1 ORDER BY name",null);
  try{while(c.moveToNext()){String id=c.getString(0),name=c.getString(1);String[] r=hrRule(id);
    mtAddLink("●",name,r[0]+" a "+r[1],()->hrSetRule(id,name));
  }}finally{c.close();}
 }
 int hrOverlap(int a,int b,int start,int end){
  return Math.max(0,Math.min(b,end)-Math.max(a,start));
 }
 int hrCommonMinutes(int a,int b,String[] rule){
  int start=rsMinutes(rule[0]),end=rsMinutes(rule[1]);
  if(start<0||end<0||b<=a)return 0;
  if(start<end)return hrOverlap(a,b,start,end);
  return hrOverlap(a,b,0,end)+hrOverlap(a,b,start,1440);
 }
 String hrTime(int minutes){return String.format(Locale.US,"%02d:%02d",minutes/60,minutes%60);}
 // Per-person per-date breakdown. Actual punch pairs are indicative pending human review,
 // especially when an overnight shift spans two civil dates.
 String[] hrDay(String pid,String day){
  String[] rule=hrRule(pid);
  java.util.ArrayList<Integer> marks=new java.util.ArrayList<>();
  Cursor c=db.getReadableDatabase().rawQuery("SELECT substr(stamp,12,5) FROM punches WHERE person_id=? AND substr(stamp,1,10)=? ORDER BY stamp",new String[]{pid,day});
  try{while(c.moveToNext()){int min=rsMinutes(c.getString(0));if(min>=0)marks.add(min);}}finally{c.close();}
  int total=0,common=0;
  for(int i=0;i+1<marks.size();i+=2){
   int a=marks.get(i),b=marks.get(i+1);
   if(b<a)continue;
   total+=b-a;common+=hrCommonMinutes(a,b,rule);
  }
  Cursor sc=db.getReadableDatabase().rawQuery("SELECT start_time,end_time FROM scheduled_shifts WHERE person_id=? AND work_date=?",new String[]{pid,day});
  boolean overnight=false;
  try{if(sc.moveToFirst()){String start=sc.getString(0),end=sc.getString(1);
   overnight=end!=null&&(end.contains("sale ")||rsMinutes(start)>=0&&rsMinutes(end)>=0&&rsMinutes(start)>rsMinutes(end));
  }}finally{sc.close();}
  String status=marks.isEmpty()?"SIN MARCAS":marks.size()%2!=0?"INCOMPLETO · REVISAR":
    overnight?"NOCTURNO · REVISAR":marks.size()>2?"PARES · REVISAR PAUSAS":"PAR · REVISAR";
  // Do not assert payable overtime from incomplete or cross-date records.
  if(overnight||marks.size()%2!=0)return new String[]{""+marks.size(),"—","—","—",status,rule[0]+"-"+rule[1]};
  return new String[]{""+marks.size(),hrTime(total),hrTime(common),hrTime(total-common),status,rule[0]+"-"+rule[1]};
 }
 void hrDashboard(Date focus){
  currentScreen="INFORMES";mtScreen("CONTROL HORARIO · MES",3);
  String from=rpDate(rpMonth(focus).getTime()),to=rpMonthEnd(focus);
  body.addView(mtText("NAUTILUS COUNTRY · CONTROL HORARIO",19,mtGold(),true));
  body.addView(mtText("Período "+from+" al "+to+" · Tabla de horas comunes y horas de recargo",13,mtPale(),false));
  mtAddLink("⚙","HORARIO COMÚN GENERAL","Configurar franja horaria para el plantel",()->hrSetRule("*","TODO EL PERSONAL"));
  mtAddLink("●","HORARIO COMÚN POR EMPLEADO","Excepciones particulares por trabajador",this::hrPersonRulePicker);
  mtAddLink("▦","CAMBIAR MES","Elegir año y mes del informe",this::chooseSummaryMonth);
  mtAddLink("▧","GENERAR PDF CON MEMBRETE","Elegí dónde guardar el documento",()->hrSavePdf(from,to,null));
  mtAddLink("◷","BUSCAR INFORME GUARDADO","Abrir un archivo desde una carpeta del teléfono",this::hrBrowseReport);
  mtAddLink("▥","ABRIR ÚLTIMO PDF GUARDADO","Abrir el último informe exportado",this::hrOpenLast);
  hrMonthTable(from,to);
 }
 void hrMonthTable(String from,String to){
  hrEnsure();
  body.addView(mtText("PLANILLA MENSUAL · TODOS LOS EMPLEADOS",15,Color.WHITE,true));
  LinearLayout header=new LinearLayout(this);header.setOrientation(LinearLayout.HORIZONTAL);
  String[] heads={"PERSONAL","COMUNES","RECARGO","REVISAR"};
  for(int i=0;i<4;i++){TextView h=mtText(heads[i],9,mtGold(),true);header.addView(h,new LinearLayout.LayoutParams(0,mtDp(34),i==0?3:2));}
  body.addView(header);
  Cursor c=db.getReadableDatabase().rawQuery("SELECT id,COALESCE(NULLIF(name,''),id) FROM people WHERE active=1 ORDER BY name",null);
  try{while(c.moveToNext()){
   String pid=c.getString(0),name=c.getString(1);int common=0,extra=0,flags=0,seen=0;
   Cursor dates=db.getReadableDatabase().rawQuery("SELECT DISTINCT substr(stamp,1,10) FROM punches WHERE person_id=? AND substr(stamp,1,10) BETWEEN ? AND ? ORDER BY 1",new String[]{pid,from,to});
   try{while(dates.moveToNext()){
    seen++;String[] v=hrDay(pid,dates.getString(0));
    if(v[1].equals("—"))flags++;
    else{common+=rsMinutes(v[2]);extra+=rsMinutes(v[3]);}
   }}finally{dates.close();}
   if(seen==0)continue;
   final String worker=pid;
   LinearLayout line=new LinearLayout(this);line.setOrientation(LinearLayout.HORIZONTAL);line.setPadding(2,mtDp(7),2,mtDp(7));
   String[] vals={name,hrTime(common),hrTime(extra),""+flags};
   for(int i=0;i<4;i++){TextView t=mtText(vals[i],i==0?12:11,Color.WHITE,i==0);t.setGravity(i==0?Gravity.START:Gravity.CENTER);
    line.addView(t,new LinearLayout.LayoutParams(0,mtDp(54),i==0?3:2));}
   line.setOnClickListener(v->hrEmployeeDetail(worker,from,to));
   body.addView(line);
  }}finally{c.close();}
  body.addView(mtText("Cifras indicativas a partir de pares de fichadas. REVISAR indica días con marcas incompletas o cruces de medianoche. No son horas liquidadas ni montos salariales.",11,mtPale(),false));
 }
 void hrEmployeeDetail(String pid,String from,String to){
  currentScreen="INFORMES";mtScreen("HORAS POR EMPLEADO",3);
  Cursor person=db.getReadableDatabase().rawQuery("SELECT name FROM people WHERE id=?",new String[]{pid});
  String name=person.moveToFirst()?person.getString(0):pid;person.close();
  body.addView(mtText(name+" · "+from+" / "+to,18,Color.WHITE,true));
  String[] rule=hrRule(pid);
  body.addView(mtText("Horario común configurado: "+rule[0]+" - "+rule[1],12,mtPale(),false));
  mtAddLink("⚙","AJUSTAR HORARIO DE "+name,"Horas comunes y recargo",()->hrSetRule(pid,name));
  mtAddLink("▧","GUARDAR PDF INDIVIDUAL","Elegir carpeta y nombre de archivo",()->hrSavePdf(from,to,pid));
  mtAddLink("◷","BUSCAR INFORME GUARDADO","Abrir desde el teléfono",this::hrBrowseReport);
  Cursor dates=db.getReadableDatabase().rawQuery("SELECT DISTINCT substr(stamp,1,10) FROM punches WHERE person_id=? AND substr(stamp,1,10) BETWEEN ? AND ? ORDER BY 1",new String[]{pid,from,to});
  try{while(dates.moveToNext()){String date=dates.getString(0),v[]=hrDay(pid,date);
   mtAddLink("▣",date,"Fich. "+v[0]+" · Comunes "+v[2]+" · Recargo "+v[3]+" · "+v[4],()->importedPunchPersonDay(pid,date));
  }}finally{dates.close();}
 }
 void hrBrowseReport(){
  Intent i=new Intent(Intent.ACTION_OPEN_DOCUMENT);
  i.setType("*/*");i.addCategory(Intent.CATEGORY_OPENABLE);
  i.addCategory(Intent.CATEGORY_DEFAULT);
  startActivityForResult(i,HR_PICK_REPORT);
 }
 void hrOpenUri(android.net.Uri uri){
  try{Intent view=new Intent(Intent.ACTION_VIEW);view.setDataAndType(uri,"application/pdf");
   view.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);startActivity(Intent.createChooser(view,"Abrir informe Nautilus"));
  }catch(Exception e){msg("No se pudo abrir","Elegí una aplicación lectora de PDF. "+e.getMessage(),this::mtReports);}
 }
 void hrOpenLast(){
  String uri=getSharedPreferences("nautilus_reports",MODE_PRIVATE).getString("last_pdf",null);
  if(uri==null){msg("Sin PDF anterior","Primero guardá un informe PDF.",this::mtReports);return;}
  hrOpenUri(android.net.Uri.parse(uri));
 }
 void hrSavePdf(String from,String to,String pid){
  try{
   hrPendingPdf=hrMakePdf(from,to,pid);
   Intent i=new Intent(Intent.ACTION_CREATE_DOCUMENT);i.addCategory(Intent.CATEGORY_OPENABLE);
   i.setType("application/pdf");
   i.putExtra(Intent.EXTRA_TITLE,"Nautilus_Control_Horas_"+from+"_"+to+(pid==null?"_Plantel":"_"+pid)+".pdf");
   startActivityForResult(i,HR_SAVE_PDF);
  }catch(Exception ex){msg("No se pudo preparar el PDF",String.valueOf(ex.getMessage()),this::mtReports);}
 }
 byte[] hrMakePdf(String from,String to,String pid)throws Exception{
  android.graphics.pdf.PdfDocument pdf=new android.graphics.pdf.PdfDocument();
  android.graphics.Paint paint=new android.graphics.Paint(3);
  int pageNo=0,row=0,y=0,count=0;
  android.graphics.Canvas canvas=null;
  android.graphics.pdf.PdfDocument.Page page=null;
  try{
   String sql="SELECT id,COALESCE(NULLIF(name,''),id) FROM people WHERE active=1 "+(pid==null?"":"AND id=? ")+"ORDER BY name";
   Cursor staff=db.getReadableDatabase().rawQuery(sql,pid==null?null:new String[]{pid});
   try{while(staff.moveToNext()){
    String id=staff.getString(0),name=staff.getString(1);
    Cursor dates=db.getReadableDatabase().rawQuery("SELECT DISTINCT substr(stamp,1,10) FROM punches WHERE person_id=? AND substr(stamp,1,10) BETWEEN ? AND ? ORDER BY 1",new String[]{id,from,to});
    try{while(dates.moveToNext()){
     if(page==null||y>738){
      if(page!=null){hrPdfFooter(canvas,paint,pageNo);pdf.finishPage(page);}
      pageNo++;page=pdf.startPage(new android.graphics.pdf.PdfDocument.PageInfo.Builder(595,842,pageNo).create());
      canvas=page.getCanvas();hrPdfHeader(canvas,paint,from,to,pageNo,pid==null?"PLANTEL COMPLETO":"INFORME INDIVIDUAL");
      y=184;
     }
     String date=dates.getString(0),v[]=hrDay(id,date);
     if(row%2==0){paint.setColor(0xFFEAF3F8);canvas.drawRect(28,y-17,567,y+8,paint);}
     hrPdfText(canvas,paint,name,31,y,10,0xFF17374C);
     hrPdfText(canvas,paint,date,233,y,9,0xFF17374C);
     hrPdfText(canvas,paint,v[2],330,y,10,0xFF124F44);
     hrPdfText(canvas,paint,v[3],400,y,10,0xFF794D11);
     hrPdfText(canvas,paint,v[4].contains("INCOMPLETO")||v[4].contains("NOCTURNO")?"REVISAR":"CONTROL",466,y,9,0xFF794D11);
     y+=29;row++;count++;
    }}finally{dates.close();}
   }}finally{staff.close();}
   if(page==null){
    pageNo++;page=pdf.startPage(new android.graphics.pdf.PdfDocument.PageInfo.Builder(595,842,pageNo).create());
    canvas=page.getCanvas();hrPdfHeader(canvas,paint,from,to,pageNo,pid==null?"PLANTEL COMPLETO":"INFORME INDIVIDUAL");
    hrPdfText(canvas,paint,"Sin fichadas registradas en este período.",34,220,14,0xFF17374C);
   }
   hrPdfFooter(canvas,paint,pageNo);pdf.finishPage(page);
   java.io.ByteArrayOutputStream out=new java.io.ByteArrayOutputStream();
   pdf.writeTo(out);return out.toByteArray();
  }finally{pdf.close();}
 }
 void hrPdfText(android.graphics.Canvas canvas,android.graphics.Paint p,String text,float x,float y,int size,int color){
  p.setColor(color);p.setTextSize(size);p.setTypeface(android.graphics.Typeface.create("sans-serif",android.graphics.Typeface.NORMAL));
  canvas.drawText(text==null?"":text.length()>31?text.substring(0,29)+"…":text,x,y,p);
 }
 void hrPdfHeader(android.graphics.Canvas c,android.graphics.Paint p,String from,String to,int page,String type){
  p.setColor(0xFF092B43);c.drawRect(0,0,595,125,p);
  p.setColor(0xFFE1B55B);c.drawRect(0,125,595,131,p);
  p.setColor(0xFFE1B55B);p.setTextSize(25);p.setTypeface(android.graphics.Typeface.create("sans-serif",android.graphics.Typeface.BOLD));
  c.drawText("NAUTILUS COUNTRY",28,49,p);
  p.setColor(0xFFFFFFFF);p.setTextSize(13);c.drawText("CONTROL HORARIO  |  FICHADAS Y RECARGOS",30,79,p);
  p.setTextSize(10);c.drawText(type+"   •   "+from+" AL "+to+"   •   PÁGINA "+page,30,105,p);
  hrPdfText(c,p,"TRABAJADOR",31,163,10,0xFF092B43);
  hrPdfText(c,p,"FECHA",233,163,10,0xFF092B43);
  hrPdfText(c,p,"COMUNES",330,163,10,0xFF092B43);
  hrPdfText(c,p,"RECARGO",400,163,10,0xFF092B43);
  hrPdfText(c,p,"ESTADO",466,163,10,0xFF092B43);
  p.setColor(0xFFB0CCD7);c.drawLine(28,174,565,174,p);
 }
 void hrPdfFooter(android.graphics.Canvas c,android.graphics.Paint p,int page){
  p.setColor(0xFF092B43);c.drawRect(0,770,595,842,p);
  hrPdfText(c,p,"HORAS INDICATIVAS - NO ES LIQUIDACIÓN DEFINITIVA",28,795,10,0xFFFFFFFF);
  hrPdfText(c,p,"Validar marcas nocturnas, pausas, incidencias y convenio. Sin importes.",28,815,9,0xFFE1B55B);
 }
'''
s=s.replace(insert,code+'\n'+insert,1)
# Intercept file saving and browsing before old handling in onActivityResult.
signature='@Override protected void onActivityResult(int q,int res,Intent data){'
assert signature in s
handler=r'''@Override protected void onActivityResult(int q,int res,Intent data){
 if(q==HR_SAVE_PDF){
  if(res==RESULT_OK&&data!=null&&data.getData()!=null&&hrPendingPdf!=null){
   try(java.io.OutputStream out=getContentResolver().openOutputStream(data.getData())){
    out.write(hrPendingPdf);out.flush();
    try{getContentResolver().takePersistableUriPermission(data.getData(),Intent.FLAG_GRANT_READ_URI_PERMISSION|Intent.FLAG_GRANT_WRITE_URI_PERMISSION);}catch(Exception ignored){}
    getSharedPreferences("nautilus_reports",MODE_PRIVATE).edit().putString("last_pdf",data.getData().toString()).apply();
    hrPendingPdf=null;
    msg("PDF guardado","El informe con membrete de Nautilus se guardó en la carpeta que elegiste. Podés abrirlo desde INFORMES.",this::mtReports);
   }catch(Exception e){msg("Error al guardar PDF",String.valueOf(e.getMessage()),this::mtReports);}
  }return;
 }
 if(q==HR_PICK_REPORT){
  if(res==RESULT_OK&&data!=null&&data.getData()!=null){
   android.net.Uri uri=data.getData();
   try{Intent view=new Intent(Intent.ACTION_VIEW);view.setDataAndType(uri,getContentResolver().getType(uri)==null?"application/pdf":getContentResolver().getType(uri));view.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);startActivity(Intent.createChooser(view,"Abrir informe"));}
   catch(Exception e){msg("No se pudo abrir el archivo",String.valueOf(e.getMessage()),this::mtReports);}
  }return;
 }
'''
s=s.replace(signature,handler,1)
# Useful entry points in actual reports and period view, show before original monthly rows.
old='''  mtAddLink("▥","INFORME MENSUAL","Elegí el año y el mes",this::chooseSummaryMonth);'''
assert old in s
s=s.replace(old,old+'''
  mtAddLink("▤","CONTROL DE HORAS Y RECARGOS","Informe con membrete, reglas y PDF",()->hrDashboard(new Date()));
  mtAddLink("◷","BUSCAR INFORME GUARDADO","Abrir archivo desde cualquier carpeta",this::hrBrowseReport);
''',1)
anchor='''  mtAddLink("●","INFORME DE UNA PERSONA","Primero elegir el empleado",()->rsPickPerson(false,f,t));'''
assert anchor in s
s=s.replace(anchor,anchor+'''
  mtAddLink("▧","PDF DE HORAS COMUNES Y RECARGO","Membrete y tablas por trabajador",()->hrSavePdf(f,t,null));
  mtAddLink("⚙","FIJAR HORARIO COMÚN","General o personalizado por empleado",()->hrDashboard(begin.getTime()));
  mtAddLink("◷","BUSCAR INFORME GUARDADO","Buscar y abrir PDF/CSV",this::hrBrowseReport);
''',1)
employee='''  mtAddLink("⇩","GUARDAR PLANILLA INDIVIDUAL","Elegir carpeta en el teléfono",()->rsSaveReport(from,to,pid));'''
assert employee in s
s=s.replace(employee,employee+'''
  mtAddLink("▧","PDF INDIVIDUAL CON MEMBRETE","Horas comunes y recargo, sin importes",()->hrSavePdf(from,to,pid));
  mtAddLink("⚙","FIJAR HORARIO COMÚN DEL EMPLEADO","Personalizar franja horaria",()->hrSetRule(pid,person));
''',1)
p.write_text(s)
print("V76 PDF branded multi-page, stored report browsing, normal/overtime hour windows individual/global; no amounts")
