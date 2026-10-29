from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()

# Track top-level screen so Back only asks to exit from HOY.
s=s.replace('public class MainActivity extends Activity{','public class MainActivity extends Activity{ String currentScreen="HOY";')
s=s.replace('void base(String title){','void base(String title){currentScreen=title;')
old=''' @Override public void onBackPressed(){
  new AlertDialog.Builder(this)
   .setTitle("Salir de Nautilus Presentismo")
   .setMessage("¿Querés salir de la aplicación?")
   .setNegativeButton("CANCELAR",null)
   .setPositiveButton("SALIR",(d,w)->finish())
   .show();
 }'''
new=''' @Override public void onBackPressed(){
  if(!"HOY".equals(currentScreen)){todayDashboard();return;}
  new AlertDialog.Builder(this).setTitle("Salir de Nautilus Presentismo").setMessage("¿Querés salir de la aplicación?")
   .setNegativeButton("CANCELAR",null).setPositiveButton("SALIR",(d,w)->finish()).show();
 }'''
assert old in s
s=s.replace(old,new)

marker=' void workerStats(){'
assert marker in s
extra=r'''
 void sectorStats(){
  base("ESTADÍSTICAS · SECTORES");
  body.addView(muted("Comparativa del mes actual por sector"));
  String ym=new SimpleDateFormat("yyyy-MM",Locale.US).format(new Date());
  Cursor sc=db.getReadableDatabase().rawQuery("SELECT id,name FROM sectors ORDER BY name",null);
  while(sc.moveToNext()){
   long sid=sc.getLong(0);String sn=sc.getString(1);int e=0,pres=0,abs=0,late=0,lateMin=0,inc=0,clock=0,rec=0;
   Cursor pc=db.getReadableDatabase().rawQuery("SELECT id FROM people WHERE active=1 AND sector_id=?",new String[]{String.valueOf(sid)});
   while(pc.moveToNext()){
    String pid=pc.getString(0);
    try{
     Calendar cal=Calendar.getInstance();cal.setTime(new SimpleDateFormat("yyyy-MM-dd",Locale.US).parse(ym+"-01"));int max=cal.getActualMaximum(Calendar.DAY_OF_MONTH);
     for(int d=1;d<=max;d++){
      DayResult r=dayResult(pid,String.format(Locale.US,"%s-%02d",ym,d));if(r==null||!r.expected)continue;
      e++;if(r.present)pres++;else abs++;if(r.lateMinutes>0){late++;lateMin+=r.lateMinutes;}if(r.incident)inc++;clock+=Math.max(0,r.clockMinutes);rec+=Math.max(0,r.recognizedMinutes);
     }
    }catch(Exception ignored){}
   }pc.close();
   double pct=e==0?0:pres*100.0/e;
   TextView v=label(String.format(Locale.US,"%s  ·  %.1f%%\nJornadas %d/%d · Ausencias %d · Tardanzas %d (%d min)\nIncidencias %d · Horas reloj %.1f · Reconocidas %.1f",sn,pct,pres,e,abs,late,lateMin,inc,clock/60.0,rec/60.0),15);
   android.graphics.drawable.GradientDrawable g=new android.graphics.drawable.GradientDrawable();g.setColor(Color.rgb(10,31,42));g.setCornerRadius(20);g.setStroke(1,pct>=95?Color.rgb(31,220,130):(pct>=85?Color.rgb(244,190,46):Color.rgb(235,67,76)));v.setBackground(g);v.setPadding(18,16,18,16);
   LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,-2);lp.setMargins(0,6,0,6);body.addView(v,lp);
  }sc.close();
 }

 void statsHub(){
  base("ESTADÍSTICAS");
  body.addView(muted("Indicadores de gestión de Nautilus Country"));
  btn("POR TRABAJADOR",this::workerStats);
  btn("POR SECTOR",this::sectorStats);
  btn("RANKING DEL PERSONAL",this::workerRanking);
  btn("RESUMEN PARA LIQUIDACIÓN",this::payrollSummary);
 }
'''
s=s.replace(marker,extra+"\n"+marker)

# Promote a statistics hub in PERSONAL/REPORTS and MORE.
s=s.replace('btn("ESTADÍSTICAS DE TRABAJADORES",this::workerStats);btn("RANKING / RESUMEN DEL PERSONAL",this::workerRanking);','btn("ESTADÍSTICAS · PERSONAL Y SECTORES",this::statsHub);')
s=s.replace('void moreMenu(){base("MÁS OPCIONES");body.addView(muted("Administración y configuración del sistema"));','void moreMenu(){base("MÁS OPCIONES");body.addView(muted("Administración y configuración del sistema"));btn("ESTADÍSTICAS",this::statsHub);')

p.write_text(s)
print("V8.5 management statistics patch applied",len(s))
