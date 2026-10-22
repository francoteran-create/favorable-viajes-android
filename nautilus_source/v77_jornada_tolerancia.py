from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
old='''  db.getWritableDatabase().execSQL("CREATE TABLE IF NOT EXISTS hour_rules(person_id TEXT PRIMARY KEY,starts TEXT NOT NULL,ends TEXT NOT NULL)");'''
assert old in s
s=s.replace(old,'''  db.getWritableDatabase().execSQL("CREATE TABLE IF NOT EXISTS hour_rules(person_id TEXT PRIMARY KEY,starts TEXT NOT NULL,ends TEXT NOT NULL,grace_minutes INTEGER DEFAULT 10)");
  try{db.getWritableDatabase().execSQL("ALTER TABLE hour_rules ADD COLUMN grace_minutes INTEGER DEFAULT 10");}catch(Exception ignored){}''',1)
assert 'String[] rule={"08:00","16:00"};' in s
s=s.replace('SELECT starts,ends FROM hour_rules','SELECT starts,ends,COALESCE(grace_minutes,10) FROM hour_rules',1)
s=s.replace('String[] rule={"08:00","16:00"};','String[] rule={"08:00","20:00","10"};',1)
s=s.replace('rule[1]=c.getString(1);','rule[1]=c.getString(1);rule[2]=c.getString(2);',1)
s=s.replace('''  body.addView(mtText("Las horas dentro del horario serán COMUNES y las restantes se informarán como RECARGO. No se calculan importes. Esta regla no modifica las fichadas ni los turnos.",13,mtPale(),false));''',
'''  body.addView(mtText("Jornada habitual 08:00 a 20:00. Podés cambiarla manualmente. Las fichadas algunos minutos antes o después NO generan extras automáticamente. Se calcula sólo el tiempo que excede la tolerancia, y queda pendiente de autorización.",13,mtPale(),false));''',1)
assert '''  EditText to=rsInput("FIN DEL HORARIO COMÚN (HH:MM)",existing[1]);''' in s
s=s.replace('''  EditText to=rsInput("FIN DEL HORARIO COMÚN (HH:MM)",existing[1]);''',
'''  EditText to=rsInput("FIN DEL HORARIO COMÚN (HH:MM)",existing[1]);
  EditText grace=rsInput("TOLERANCIA DE ENTRADA Y SALIDA (MINUTOS)",existing[2]);''',1)
s=s.replace('''   ContentValues v=new ContentValues();v.put("person_id",pid);v.put("starts",start);v.put("ends",end);''',
'''   int tolerance=-1;try{tolerance=Integer.parseInt(grace.getText().toString().trim());}catch(Exception ignored){}
   if(tolerance<0||tolerance>120){msg("Tolerancia inválida","Usá entre 0 y 120 minutos.",()->hrSetRule(pid,title));return;}
   ContentValues v=new ContentValues();v.put("person_id",pid);v.put("starts",start);v.put("ends",end);v.put("grace_minutes",tolerance);''',1)
s=s.replace('''Las horas fuera de esta franja se reportarán como recargo, sujetas a revisión.''','''Tolerancia "+tolerance+" minutos. Los recargos son sólo indicativos y requieren aprobación.''',1)
# Replace the core classification: floor ordinary range at configured hours; outside = EXCESS over grace,
# not the first ten minutes before/after a jornada; both still remain raw punch evidence.
old='''  int total=0,common=0;
  for(int i=0;i+1<marks.size();i+=2){
   int a=marks.get(i),b=marks.get(i+1);
   if(b<a)continue;
   total+=b-a;common+=hrCommonMinutes(a,b,rule);
  }'''
new='''  int total=0,common=0,extra=0;
  int shiftStart=rsMinutes(rule[0]),shiftEnd=rsMinutes(rule[1]);
  int tolerance=10;try{tolerance=Integer.parseInt(rule[2]);}catch(Exception ignored){}
  for(int i=0;i+1<marks.size();i+=2){
   int a=marks.get(i),b=marks.get(i+1);
   if(b<a)continue;
   total+=b-a;common+=hrCommonMinutes(a,b,rule);
   if(shiftStart>=0&&shiftEnd>shiftStart){
    // Tolerance is a deadband. An employee clocking in at 07:50 or out at 20:10
    // with the default configuration receives ZERO overtime, not 10 minutes.
    extra+=Math.max(0,Math.min(b,shiftStart-tolerance)-a);
    extra+=Math.max(0,b-Math.max(a,shiftEnd+tolerance));
   }
  }'''
assert old in s
s=s.replace(old,new,1)
s=s.replace('''hrTime(total),hrTime(common),hrTime(total-common),status''',
'''hrTime(total),hrTime(common),hrTime(extra),status''',1)
# Label any candidate overtime as UNAPPROVED so it isn't treated as payable.
s=s.replace('''marks.size()>2?"PARES · REVISAR PAUSAS":"PAR · REVISAR";''',
'''marks.size()>2?"PARES · REVISAR PAUSAS":extra>0?"RECARGO PROPUESTO · SIN APROBAR":"DENTRO DE TOLERANCIA";''',1)
s=s.replace('''body.addView(mtText("Horario común configurado: "+rule[0]+" - "+rule[1],12,mtPale(),false));''',
'''body.addView(mtText("Jornada común: "+rule[0]+" - "+rule[1]+" · Tolerancia: "+rule[2]+" min (entrada/salida)",12,mtPale(),false));''',1)
s=s.replace('''"Cifras indicativas a partir de pares de fichadas. REVISAR indica días con marcas incompletas o cruces de medianoche. No son horas liquidadas ni montos salariales."''',
'''"Cifras orientativas: la tolerancia no genera recargo. El recargo calculado NO está aprobado para liquidación. REVISAR marcas incompletas, pausas y horarios nocturnos. Nunca se calculan importes."''',1)
# Offer the configuration where employee shifts are assigned, not just reports.
anchor='''  body.addView(mtText(person+" · ID "+pid,19,Color.WHITE,true));'''
assert anchor in s
s=s.replace(anchor,anchor+'''
  mtAddLink("⚙","HORARIO COMÚN Y TOLERANCIA","08:00 a 20:00 · 10 minutos por defecto · editable",()->hrSetRule(pid,person));''',1)
p.write_text(s)
print("V77: 08-20 default normal day, editable shift and grace 10 minutes; recargos proposed never payable automatically")
