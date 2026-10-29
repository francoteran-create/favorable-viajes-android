from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
needle='''  if(last>now+10*60*1000L)return false;'''
assert needle in s
s=s.replace(needle,'''  if(last>now+10*60*1000L)return false;
  if(now<1609459200000L)return false; // reject clearly invalid date (before 2021)
''',1)
needle='''  return now<until;
 }
 boolean licAccept'''
assert needle in s
s=s.replace(needle,'''  return now<until;
 }
 String licStatus(){
  long end=licPrefs().getLong("until",0);
  if(end<=0)return "Prueba inicial: 3 meses desde el primer uso";
  java.text.SimpleDateFormat df=new java.text.SimpleDateFormat("dd/MM/yyyy",new java.util.Locale("es","AR"));
  df.setTimeZone(java.util.TimeZone.getTimeZone("America/Argentina/Buenos_Aires"));
  long remain=Math.max(0L,(end-System.currentTimeMillis()+86399999L)/86400000L);
  return "Licencia hasta "+df.format(new java.util.Date(end))+" · "+remain+" día(s) restantes";
 }
 boolean licAccept''',1)
needle='''  new AlertDialog.Builder(this).setTitle("LICENCIA VENCIDA")'''
assert needle in s
s=s.replace(needle,'''  new AlertDialog.Builder(this).setTitle("LICENCIA VENCIDA")''',1)
needle='''.setView(input).setCancelable(false).setNegativeButton("VOLVER",(d,w)->secLogin())'''
assert needle in s
s=s.replace(needle,'''.setMessage(index==0?"Acceso permanente del DESARROLLADOR":licStatus())
   .setView(input).setCancelable(false).setNegativeButton("VOLVER",(d,w)->secLogin())''',1)
p.write_text(s)
print("V98 license validation and expiry status helper")
