from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
old='String[] cycles={"5x2 · trabaja 5 / franco 2","4x2 · trabaja 4 / franco 2","6x1 · trabaja 6 / franco 1","TODOS LOS DÍAS · sin francos","MANUAL · por día desde calendario"};'
new='String[] cycles={"5x2 · 5 días de trabajo / 2 francos","4x2 · 4 días de trabajo / 2 francos","6x1 · 6 días de trabajo / 1 franco","TODOS LOS DÍAS","12x24 hs · 12 horas de trabajo / 24 de descanso","12x36 hs · 12 horas de trabajo / 36 de descanso","24x48 hs · 24 horas de trabajo / 48 de descanso","24x72 hs · 24 horas de trabajo / 72 de descanso","8x16 hs · 8 horas de trabajo / 16 de descanso","12x12 hs · 12 horas de trabajo / 12 de descanso","2x2 días · 2 de trabajo / 2 francos","3x3 días · 3 de trabajo / 3 francos","MANUAL · por día desde calendario"};'
assert old in s
s=s.replace(old,new,1)
s=s.replace('''  body.addView(mtText("En turnos nocturnos la salida puede ser al día siguiente (ejemplo 22:00 a 06:00). Los francos se generan desde la fecha de inicio elegida.",12,mtPale(),false));''',
'''  body.addView(mtText("En rotaciones por HORAS, indicá la hora de la PRIMERA entrada: el sistema calcula automáticamente las siguientes entradas, las salidas y el descanso, aunque crucen la medianoche. En rotaciones por DÍAS, completá entrada y salida.",12,mtPale(),false));''',1)
old='''    int selected=cycle.getSelectedItemPosition(),on=selected==0?5:selected==1?4:selected==2?6:selected==3?1:0;
    int off=selected==0?2:selected==1?2:selected==2?1:0;
    if(selected==4){mtCalendar(c.getTime());return;}
    String regime=selected==0?"5x2":selected==1?"4x2":selected==2?"6x1":"TODOS";'''
new='''    int selected=cycle.getSelectedItemPosition();
    if(selected>=4&&selected<=9){
     int[] work={12,12,24,24,8,12},rest={24,36,48,72,16,12};
     int idx=selected-4;
     rsGenerateHourly(pid,person,d,amount,a,work[idx],rest[idx]);return;
    }
    if(selected==12){mtCalendar(c.getTime());return;}
    int on=selected==0?5:selected==1?4:selected==2?6:selected==3?1:selected==10?2:3;
    int off=selected==0?2:selected==1?2:selected==2?1:selected==3?0:selected==10?2:3;
    String regime=selected==0?"5x2":selected==1?"4x2":selected==2?"6x1":selected==3?"TODOS":selected==10?"2x2":"3x3";'''
assert old in s
s=s.replace(old,new,1)
# The visual end time is informational for hourly cycle: calculations derive from start and work duration.
anchor=''' void rsPersonPlan(String pid,String focus){'''
assert anchor in s
code=r'''
 void rsGenerateHourly(String pid,String person,String day,int amount,String start,int workHours,int restHours){
  rsEnsure();
  try{
   SimpleDateFormat formatter=new SimpleDateFormat("yyyy-MM-dd HH:mm",Locale.US);
   formatter.setLenient(false);
   java.util.Date anchor=formatter.parse(day+" "+start);
   if(anchor==null)throw new Exception("Fecha u hora de comienzo inválida.");
   long startMs=anchor.getTime(),intervalMs=((long)workHours+restHours)*3600000L;
   long workMs=(long)workHours*3600000L,endPeriod=startMs+(long)amount*86400000L;
   String regime=workHours+"x"+restHours+" hs";
   SimpleDateFormat dateFormat=new SimpleDateFormat("yyyy-MM-dd",Locale.US);
   SimpleDateFormat timeFormat=new SimpleDateFormat("HH:mm",Locale.US);
   SQLiteDatabase w=db.getWritableDatabase();int count=0;
   w.beginTransaction();
   try{
    for(long when=startMs;when<endPeriod;when+=intervalMs){
     java.util.Date entry=new java.util.Date(when),exit=new java.util.Date(when+workMs);
     String beginDay=dateFormat.format(entry),finishDay=dateFormat.format(exit);
     String finish=timeFormat.format(exit)+(beginDay.equals(finishDay)?"":" (sale "+finishDay+")");
     ContentValues v=new ContentValues();
     v.put("person_id",pid);v.put("work_date",beginDay);v.put("start_time",timeFormat.format(entry));
     v.put("end_time",finish);v.put("cycle_name",regime);
     w.insertWithOnConflict("scheduled_shifts",null,v,SQLiteDatabase.CONFLICT_REPLACE);
     count++;
    }
    w.setTransactionSuccessful();
   }finally{w.endTransaction();}
   msg("Rotación horaria guardada",person+" · "+regime+
    "\nTurnos generados: "+count+
    "\nPrimera entrada: "+day+" "+start+
    "\nLas siguientes entradas respetan "+restHours+" horas completas de descanso."+
    "\nLa fecha de salida indica los turnos nocturnos o de 24 horas.",()->rsPersonPlan(pid,day));
  }catch(Exception error){msg("No se pudo generar la rotación",String.valueOf(error.getMessage()),()->rsSetup(pid));}
 }
'''
s=s.replace(anchor,code+'\n'+anchor,1)
# Better daily description of cyclic shifts with a separate date of exit.
s=s.replace('mtAddLink("▣",day,start.equals("FRANCO")?"FRANCO · "+regime:start+" — "+end+" · "+regime,()->rsEditDay(pid,day));',
'''mtAddLink("▣",day,start.equals("FRANCO")?"FRANCO · "+regime:start+" — "+end+" · "+regime,()->rsEditDay(pid,day));''',1)
p.write_text(s)
print("V74: expanded day-based and hour-based rotation formulas, crossing-midnight output, no raw punches modified")
