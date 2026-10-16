from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void btn(String s,Runnable r){'
assert mark in s
code=r'''
 void backupScreen(){
  base("BACKUP / RESTAURAR");sectionTitle("COPIA DE SEGURIDAD","Protección de la base de presentismo");
  body.addView(premiumCard("BASE LOCAL","NAUTILUS PRESENTISMO","Empleados · fichadas · turnos · incidencias",Color.rgb(48,205,166)));
  addRefRow("↓","Crear backup","Genera una copia completa de la base local","CREAR",Color.rgb(48,205,166),this::createBackup);
  addRefRow("↑","Restaurar backup","Seleccionar una copia previamente guardada","ELEGIR",Color.rgb(244,190,46),this::pickBackup);
  body.addView(muted("La restauración reemplaza la base local. Las fichadas originales permanecen dentro de la copia seleccionada."));
 }
 void createBackup(){
  try{java.io.File src=getDatabasePath("nautilus.db");if(!src.exists()){toast("Todavía no existe base para copiar");return;}java.io.File dir=new java.io.File(getExternalFilesDir(null),"backups");dir.mkdirs();String stamp=new SimpleDateFormat("yyyyMMdd-HHmmss",Locale.US).format(new Date());java.io.File dst=new java.io.File(dir,"Nautilus-Backup-"+stamp+".db");java.io.FileInputStream in=new java.io.FileInputStream(src);java.io.FileOutputStream out=new java.io.FileOutputStream(dst);byte[] buf=new byte[8192];int n;while((n=in.read(buf))>0)out.write(buf,0,n);in.close();out.close();toast("Backup creado: "+dst.getName());}catch(Exception e){toast("No se pudo crear backup: "+e.getMessage());}
 }
 void pickBackup(){
  Intent i=new Intent(Intent.ACTION_OPEN_DOCUMENT);i.setType("*/*");i.addCategory(Intent.CATEGORY_OPENABLE);startActivityForResult(i,901);
 }
 void restoreBackup(Uri uri){
  try{java.io.InputStream in=getContentResolver().openInputStream(uri);if(in==null){toast("No se pudo abrir el backup");return;}db.close();java.io.File dst=getDatabasePath("nautilus.db");java.io.FileOutputStream out=new java.io.FileOutputStream(dst,false);byte[] buf=new byte[8192];int n;while((n=in.read(buf))>0)out.write(buf,0,n);in.close();out.close();db=new DB(this);toast("Backup restaurado");todayDashboard();}catch(Exception e){toast("No se pudo restaurar: "+e.getMessage());}
 }
'''
s=s.replace(mark,code+"\n"+mark)
# Replace provisional backup routing with real backup screen.
s=s.replace('addRefRow("↻","Backup / Restaurar","Copia de seguridad de datos","›",Color.rgb(244,190,46),this::logs);','addRefRow("↻","Backup / Restaurar","Copia de seguridad de datos","›",Color.rgb(244,190,46),this::backupScreen);')
# Hook activity result without disturbing existing import handler: inject at beginning if method exists.
needle='protected void onActivityResult(int requestCode,int resultCode,Intent data){super.onActivityResult(requestCode,resultCode,data);'
if needle in s:s=s.replace(needle,needle+'if(requestCode==901&&resultCode==RESULT_OK&&data!=null&&data.getData()!=null){new AlertDialog.Builder(this).setTitle("Restaurar backup").setMessage("Esto reemplazará la base local actual. ¿Continuar?").setNegativeButton("CANCELAR",null).setPositiveButton("RESTAURAR",(d,w)->restoreBackup(data.getData())).show();return;}')
# If actual DB filename differs, derive it from helper DB name at runtime by using getDatabasePath known from SQLiteOpenHelper constructor replacement.
import re
m=re.search(r'super\(c,"([^"]+)"',s)
if m:s=s.replace('getDatabasePath("nautilus.db")',f'getDatabasePath("{m.group(1)}")')
s=s.replace('V17 REACTOR','V18 HARDENED')
p.write_text(s)
print("V18 backup restore hardening applied")
