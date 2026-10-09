from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# Install crash recorder before any database/UI startup work.
needle="setContentView(root);"
assert needle in s
handler=r'''
  Thread.setDefaultUncaughtExceptionHandler((thread,error)->{
   try{
    java.io.File f=new java.io.File(getFilesDir(),"nautilus_crash.txt");
    java.io.PrintWriter w=new java.io.PrintWriter(new java.io.FileWriter(f,false));
    w.println(new java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss",java.util.Locale.US).format(new java.util.Date()));
    error.printStackTrace(w);w.close();
   }catch(Exception ignored){}
   android.os.Process.killProcess(android.os.Process.myPid());
   System.exit(10);
  });
'''
s=s.replace(needle,needle+"\n"+handler,1)
# Safe boot: don't execute the increasingly complex live dashboard as first instruction.
# Keep DB initialization intact, then route initial home to a minimal diagnostic-safe launcher if exactToday is directly called.
mark=' void btn(String s,Runnable r){';assert mark in s
code=r'''
 void safeBootHome(){
  try{
   base("NAUTILUS COUNTRY","Presentismo");
   applyNautilusHomeSkin();
   TextView ok=label("SISTEMA INICIADO",20);ok.setTextColor(Color.rgb(80,220,180));ok.setGravity(Gravity.CENTER);body.addView(ok);
   TextView sub=label("Inicio seguro · V49\nSi ves esta pantalla, el arranque Android y la base principal están funcionando.",13);sub.setTextColor(Color.WHITE);sub.setGravity(Gravity.CENTER);body.addView(sub);
   Button enter=homeFeature("ENTRAR AL SISTEMA","Abrir panel completo",this::exactToday);body.addView(enter,new LinearLayout.LayoutParams(-1,96));
   Button crash=homeFeature("VER DIAGNÓSTICO","Mostrar último error guardado",this::showLastCrash);body.addView(crash,new LinearLayout.LayoutParams(-1,86));
  }catch(Throwable e){android.widget.Toast.makeText(this,"NAUTILUS V49: "+e.getClass().getSimpleName()+" "+e.getMessage(),android.widget.Toast.LENGTH_LONG).show();}
 }
 void showLastCrash(){
  try{java.io.File f=new java.io.File(getFilesDir(),"nautilus_crash.txt");if(!f.exists()){msg("Diagnóstico","No hay un error guardado.");return;}java.io.BufferedReader r=new java.io.BufferedReader(new java.io.FileReader(f));StringBuilder b=new StringBuilder();String x;while((x=r.readLine())!=null)b.append(x).append("\n");r.close();msg("Último error",b.toString());}catch(Exception e){msg("Diagnóstico",e.toString());}
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Replace only first startup exactToday invocation after onCreate region with safeBootHome.
start=s.find("void onCreate")
end=s.find("\n }",start)
segment=s[start:end]
idx=segment.rfind("exactToday();")
if idx>=0:
 segment=segment[:idx]+"safeBootHome();"+segment[idx+len("exactToday();"):]
 s=s[:start]+segment+s[end:]
s=s.replace("V48.1 RELEASE COMPILE FIX","V49 SAFE BOOT DIAGNOSTIC")
p.write_text(s);print("V49 safe boot + persistent crash diagnostic installed")
