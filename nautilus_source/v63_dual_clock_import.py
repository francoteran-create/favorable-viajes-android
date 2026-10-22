from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=" void mtConfig(){"
assert mark in s
code=r'''
 static final int PICK_PERSONNEL_REPORT=914;
 void dualClockHub(){
  currentScreen="IMPORTAR";mtScreen("IMPORTAR DATOS DEL RELOJ",4);
  body.addView(mtText("Podés seleccionar ambos archivos en cualquier orden. Se cruzan por ID del reloj y no se duplican empleados ni fichadas.",13,mtPale(),false));
  mtAddLink("1","ATTENDANCE REPORT.XLS","Importar nombres y sectores/departamentos",this::pickPersonnelReport);
  mtAddLink("2","ATTENDANCE LOGS.XLS","Importar marcaciones de entrada y salida",this::pick);
  mtAddLink("●","REVISAR PERSONAL","Ver empleados y completar datos faltantes",this::mtPersonnel);
  body.addView(mtText("Si un sector importado no coincide con uno configurado manualmente, se conserva el actual y se informa el conflicto. Los regímenes de turno no se deducen de las fichadas.",12,mtPale(),false));
 }
 void pickPersonnelReport(){
  Intent i=new Intent(Intent.ACTION_OPEN_DOCUMENT);i.setType("*/*");i.addCategory(Intent.CATEGORY_OPENABLE);
  startActivityForResult(i,PICK_PERSONNEL_REPORT);
 }
 String normalizeClockSector(String v){
  String t=java.text.Normalizer.normalize(v.trim(),java.text.Normalizer.Form.NFD).replaceAll("\\p{M}","").toLowerCase(Locale.ROOT);
  if(t.startsWith("segur"))return "Seguridad";
  if(t.startsWith("manteni"))return "Mantenimiento";
  if(t.startsWith("administra"))return "Administración";
  if(t.startsWith("limpie"))return "Limpieza";
  if(t.startsWith("jardin"))return "Jardinería";
  return "";
 }
 String clockPersonReportResult="";
 int importPersonnelReport(InputStream in)throws Exception{
  DocumentBuilderFactory factory=DocumentBuilderFactory.newInstance();factory.setNamespaceAware(true);
  factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl",true);
  factory.setFeature("http://xml.org/sax/features/external-general-entities",false);
  factory.setFeature("http://xml.org/sax/features/external-parameter-entities",false);
  factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd",false);
  factory.setXIncludeAware(false);factory.setExpandEntityReferences(false);
  org.w3c.dom.Document doc=factory.newDocumentBuilder().parse(in);
  org.w3c.dom.NodeList rows=doc.getElementsByTagNameNS("*","Row");
  java.util.regex.Pattern heading=java.util.regex.Pattern.compile("ID\\.:\\s*(\\d+)\\s+Name:\\s*(.*?)\\s+Dept\\.Name:\\s*(.*)",java.util.regex.Pattern.CASE_INSENSITIVE);
  java.util.LinkedHashMap<String,String[]> found=new java.util.LinkedHashMap<>();
  for(int k=0;k<rows.getLength();k++){
   ArrayList<String> cells=row((Element)rows.item(k));
   for(String cell:cells){
    java.util.regex.Matcher m=heading.matcher(cell);
    if(m.find()){String id=m.group(1).trim();String name=m.group(2).trim();String dept=m.group(3).trim();
     if(!id.isEmpty()&&!name.isEmpty())found.put(id,new String[]{name,dept});break;}
   }
  }
  if(found.isEmpty())throw new IOException("No se encontraron filas de personal con ID., Name y Dept.Name. Seleccioná Attendance Report.xls.");
  ensurePersonnelMaster();SQLiteDatabase w=db.getWritableDatabase();
  int created=0,assigned=0,unknown=0,conflicts=0,renamed=0;
  w.beginTransaction();
  try{
   for(java.util.Map.Entry<String,String[]> entry:found.entrySet()){
    String id=entry.getKey(),name=entry.getValue()[0],rawDept=entry.getValue()[1];
    String sector=normalizeClockSector(rawDept);
    Cursor existing=w.rawQuery("SELECT name,sector_id FROM people WHERE id=?",new String[]{id});
    boolean isNew=!existing.moveToFirst();
    String currentName=isNew?"":existing.getString(0);
    boolean hasSector=!isNew&&!existing.isNull(1);
    existing.close();
    if(isNew){
     ContentValues v=new ContentValues();v.put("id",id);v.put("name",name);v.put("active",1);
     w.insertOrThrow("people",null,v);created++;
    }else if(currentName==null||currentName.trim().isEmpty()||currentName.startsWith("Empleado ")){
     ContentValues v=new ContentValues();v.put("name",name);w.update("people",v,"id=?",new String[]{id});renamed++;
    }
    if(sector.isEmpty()){unknown++;continue;}
    Cursor sec=w.rawQuery("SELECT id FROM sectors WHERE name=? LIMIT 1",new String[]{sector});
    if(!sec.moveToFirst()){sec.close();unknown++;continue;}
    int sectorId=sec.getInt(0);sec.close();
    if(hasSector){
     Cursor cur=w.rawQuery("SELECT sector_id FROM people WHERE id=?",new String[]{id});
     if(cur.moveToFirst()&&!cur.isNull(0)&&cur.getInt(0)!=sectorId)conflicts++;
     cur.close();
    }else{
     ContentValues v=new ContentValues();v.put("sector_id",sectorId);
     w.update("people",v,"id=?",new String[]{id});assigned++;
    }
   }
   w.setTransactionSuccessful();
  }finally{w.endTransaction();}
  clockPersonReportResult="Empleados identificados: "+found.size()+"\nAltas nuevas: "+created+
   "\nSectores asignados: "+assigned+"\nNombres completados: "+renamed+
   "\nSectores no reconocidos: "+unknown+"\nConflictos (se conservaron los existentes): "+conflicts;
  return found.size();
 }
'''
s=s.replace(mark,code+"\n"+mark,1)
# Install independent document-picker callback ahead of existing punch/photo import processing.
m=re.search(r'\bvoid\s+onActivityResult\s*\(\s*int\s+(\w+)\s*,\s*int\s+(\w+)\s*,\s*Intent\s+(\w+)\s*\)\s*\{',s)
assert m
q,r,d=m.groups()
handler=f'''if({q}==PICK_PERSONNEL_REPORT){{if({r}==RESULT_OK&&{d}!=null&&{d}.getData()!=null){{try(InputStream stream=getContentResolver().openInputStream({d}.getData())){{importPersonnelReport(stream);msg("Personal y sectores importados",clockPersonReportResult,()->dualClockHub());}}catch(Exception error){{msg("No se pudo importar el reporte",error.getMessage(),this::dualClockHub);}}}}return;}}'''
s=s[:m.end()]+handler+s[m.end():]
# All entry points in current modern home and config lead to new hub, not day attendance.
s=s.replace('mtFeature("⇩","IMPORTAR FICHADAS","Reloj biométrico",()->attendance(new Date()),false)', 'mtFeature("⇩","IMPORTAR DATOS","Personal y fichadas del reloj",this::dualClockHub,false)')
s=s.replace('mtAddLink("⇩","IMPORTAR FICHADAS","Archivo descargado del reloj biométrico",()->attendance(new Date()))','mtAddLink("⇩","IMPORTAR DATOS DEL RELOJ","Dos archivos: empleados y fichadas",this::dualClockHub)')
# Existing PICK callback remains source-of-truth for idempotent punches.
# Make original success dialog return to the new import hub instead of historic personnel screen.
s=s.replace('this::mtPersonnel);}catch(Exception e){msg("No se pudo importar"','this::dualClockHub);}catch(Exception e){msg("No se pudo importar"')
p.write_text(s)
print("V63 dual clock import report + existing logs, ID merge, conflict-safe sector mapping")
