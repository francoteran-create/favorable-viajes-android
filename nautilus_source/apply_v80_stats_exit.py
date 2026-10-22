from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()

# Add Android back handling with explicit exit confirmation.
marker=" static class DayResult{"
assert marker in s
helper=r'''
 @Override public void onBackPressed(){
  new AlertDialog.Builder(this)
   .setTitle("Salir de Nautilus Presentismo")
   .setMessage("¿Querés salir de la aplicación?")
   .setNegativeButton("CANCELAR",null)
   .setPositiveButton("SALIR",(d,w)->finish())
   .show();
 }

 void workerStats(){
  base("ESTADÍSTICAS · PERSONAL");
  body.addView(muted("Resumen por trabajador · mes actual"));
  String ym=new SimpleDateFormat("yyyy-MM",Locale.US).format(new Date());
  Cursor pc=db.getReadableDatabase().rawQuery("SELECT id,name FROM people WHERE active=1 ORDER BY name",null);
  while(pc.moveToNext()){
   String pid=pc.getString(0),name=pc.getString(1);
   int expected=0,present=0,absent=0,late=0,lateMin=0,clockMin=0,recognizedMin=0,inc=0;
   Calendar cal=Calendar.getInstance();
   try{
    Date first=new SimpleDateFormat("yyyy-MM-dd",Locale.US).parse(ym+"-01");cal.setTime(first);
    int max=cal.getActualMaximum(Calendar.DAY_OF_MONTH);
    for(int d=1;d<=max;d++){
     String day=String.format(Locale.US,"%s-%02d",ym,d);
     DayResult r=dayResult(pid,day);
     if(r==null||!r.expected)continue;
     expected++;
     if(r.present)present++; else absent++;
     if(r.lateMinutes>0){late++;lateMin+=r.lateMinutes;}
     clockMin+=Math.max(0,r.clockMinutes);
     recognizedMin+=Math.max(0,r.recognizedMinutes);
     if(r.incident)inc++;
    }
   }catch(Exception ignored){}
   double pct=expected==0?0:(present*100.0/expected);
   TextView card=label(String.format(Locale.US,"%s\nPresentismo %.1f%% · %d/%d jornadas\nAusencias %d · Tardanzas %d (%d min) · Incidencias %d\nHoras reloj %.1f · Reconocidas %.1f",name,pct,present,expected,absent,late,lateMin,inc,clockMin/60.0,recognizedMin/60.0),15);
   android.graphics.drawable.GradientDrawable cg=new android.graphics.drawable.GradientDrawable();cg.setColor(Color.rgb(10,31,42));cg.setCornerRadius(20);cg.setStroke(1,pct>=95?Color.rgb(31,220,130):(pct>=85?Color.rgb(244,190,46):Color.rgb(235,67,76)));card.setBackground(cg);card.setPadding(18,16,18,16);
   LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(-1,-2);cp.setMargins(0,6,0,6);body.addView(card,cp);
  }
  pc.close();
 }

 void workerRanking(){
  base("RANKING · PERSONAL");
  body.addView(muted("Indicadores del mes actual para gestión. No altera fichadas ni liquidación."));
  String ym=new SimpleDateFormat("yyyy-MM",Locale.US).format(new Date());
  ArrayList<String> rows=new ArrayList<>();
  Cursor pc=db.getReadableDatabase().rawQuery("SELECT id,name FROM people WHERE active=1 ORDER BY name",null);
  while(pc.moveToNext()){
   String pid=pc.getString(0),name=pc.getString(1);int e=0,pres=0,a=0,t=0,tm=0,inc=0;
   try{
    Calendar cal=Calendar.getInstance();cal.setTime(new SimpleDateFormat("yyyy-MM-dd",Locale.US).parse(ym+"-01"));int max=cal.getActualMaximum(Calendar.DAY_OF_MONTH);
    for(int d=1;d<=max;d++){DayResult r=dayResult(pid,String.format(Locale.US,"%s-%02d",ym,d));if(r==null||!r.expected)continue;e++;if(r.present)pres++;else a++;if(r.lateMinutes>0){t++;tm+=r.lateMinutes;}if(r.incident)inc++;}
   }catch(Exception ignored){}
   double pct=e==0?0:pres*100.0/e;rows.add(String.format(Locale.US,"%06.2f|%s|%.1f%% · Aus %d · Tard %d/%d min · Inc %d",100-pct,name,pct,a,t,tm,inc));
  }pc.close();java.util.Collections.sort(rows);
  int pos=1;for(String x:rows){String[] z=x.split("\\|",3);TextView v=label(pos+".  "+z[1]+"\n"+z[2],15);v.setPadding(14,12,14,12);body.addView(v);pos++;}
 }
'''
s=s.replace(marker,helper+"\n"+marker)

# Add visible statistics entries to PERSONAL and reports.
needle='void employees(){base("PERSONAL");'
assert needle in s
s=s.replace(needle,'void employees(){base("PERSONAL");btn("ESTADÍSTICAS DE TRABAJADORES",this::workerStats);btn("RANKING / RESUMEN DEL PERSONAL",this::workerRanking);')
# Add shortcut in reports if recognizable.
s=s.replace('void reports(){base("INFORMES");','void reports(){base("INFORMES");btn("ESTADÍSTICAS DE TRABAJADORES",this::workerStats);btn("RANKING / RESUMEN DEL PERSONAL",this::workerRanking);')

p.write_text(s)
print("V8 behavior/statistics patch applied",len(s))
