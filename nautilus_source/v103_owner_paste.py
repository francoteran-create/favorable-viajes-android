from pathlib import Path
import os
j=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=j.read_text()
needle='''    .setNegativeButton("VOLVER",(x,y)->secLogin())
    .setPositiveButton("AUTORIZAR ESTE TELÉFONO",(x,y)->{'''
assert needle in s
s=s.replace(needle,'''    .setNegativeButton("VOLVER",(x,y)->secLogin())
    .setNeutralButton("PEGAR CLAVE PRIVADA",(x,y)->licPasteOwnerKey())
    .setPositiveButton("IMPORTAR CLAVE",(x,y)->{''',1)
mark=' void licImportOwnerKey(){'
assert mark in s
code=r'''
 void licPasteOwnerKey(){
  android.widget.EditText input=new android.widget.EditText(this);
  input.setHint("Pegá tu clave privada original (PEM)");
  input.setMinLines(4);
  input.setInputType(android.text.InputType.TYPE_CLASS_TEXT|
    android.text.InputType.TYPE_TEXT_FLAG_MULTI_LINE|
    android.text.InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD);
  new AlertDialog.Builder(this).setTitle("AUTORIZACIÓN EXCLUSIVA")
   .setMessage("Una única vez. La clave se cifra dentro del teléfono y nunca se envía.")
   .setView(input).setCancelable(false)
   .setNegativeButton("CANCELAR",(d,w)->{securityOwner=false;securityUnlocked=false;securityPromptOpen=false;secGate();})
   .setPositiveButton("VALIDAR",(d,w)->{
     try{
      byte[] pem=input.getText().toString().getBytes(java.nio.charset.StandardCharsets.UTF_8);
      if(pem.length<100||pem.length>8192)throw new Exception("Formato o tamaño incorrecto");
      licSaveEncryptedOwner(pem);
      java.util.Arrays.fill(pem,(byte)0);
      if(!licDeveloperAuthorized())throw new Exception("La clave no coincide con Nautilus");
      securityOwner=true;securityUnlocked=true;securityPromptOpen=true;
      if(!secPrefs().contains("owner_hash"))secEnroll();else secAdminPanel();
     }catch(Exception ex){
      new java.io.File(getFilesDir(),"nautilus_owner_private.enc").delete();
      securityOwner=false;securityUnlocked=false;securityPromptOpen=false;
      new AlertDialog.Builder(this).setTitle("NO AUTORIZADO")
       .setMessage("La clave proporcionada no corresponde al generador original.")
       .setPositiveButton("VOLVER",(a,b)->secLogin()).show();
     }finally{input.setText("");}
   }).show();
 }
'''
s=s.replace(mark,code+mark,1)
j.write_text(s)
print("V103 one-time encrypted owner provisioning via paste or import")
