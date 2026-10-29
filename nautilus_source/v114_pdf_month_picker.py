from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
anchor="void generateFormalPdf(){"
assert s.count(anchor)==1,"PDF exporter changed"
method=r'''
 void mtPdfMonthSelect(int year){
  if(year<2020||year>2100){return;}
  currentScreen="INFORMES";
  mtScreen("GUARDAR INFORME PDF · ELEGIR MES",3);
  body.addView(mtText("Elegí el mes a exportar. El PDF incluye jornadas por empleado y total del plantel, y se guarda en la carpeta que selecciones.",13,mtPale(),false));
  mtAddLink("‹","AÑO ANTERIOR","Ver meses de "+(year-1),()->mtPdfMonthSelect(year-1));
  body.addView(mtText("AÑO "+year,19,Color.WHITE,true));
  String[] months={"ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"};
  for(int i=0;i<months.length;i++){
   final String ym=String.format(Locale.US,"%04d-%02d",year,i+1);
   final String label=months[i]+" "+year;
   mtAddLink("▣",label,"GENERAR Y GUARDAR PDF",()->{
    selectedYm=ym;
    generateFormalPdf();
   });
  }
  mtAddLink("›","AÑO SIGUIENTE","Ver meses de "+(year+1),()->mtPdfMonthSelect(year+1));
 }
 void mtPdfMonthSelect(){
  java.util.Calendar c=java.util.Calendar.getInstance();
  mtPdfMonthSelect(c.get(java.util.Calendar.YEAR));
 }
'''
s=s.replace(anchor,method+"\n "+anchor,1)
import re
m=re.search(r'\bvoid\s+mtReports\s*\(\s*\)\s*\{',s)
assert m,"Modern report menu missing"
start=m.end()
entry=s.find("mtScreen(",start,start+350)
assert entry>=0,"Modern reports screen constructor missing"
place=s.find(";",entry)
assert place>=0 and place<start+450,"Modern reports screen constructor moved"
s=s[:place+1]+'''
  mtAddLink("◧","PDF MENSUAL","Elegir año, mes y carpeta de destino",this::mtPdfMonthSelect);
'''+s[place+1:]
p.write_text(s)
print("V114: report menu provides year/month selection and direct PDF export to user-selected folder")
