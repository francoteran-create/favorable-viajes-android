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
item='mtAddLink("◧","DOCUMENTO PDF","Preparar informe imprimible",this::reports);'
assert item in s,"Modern reports PDF link changed"
s=s.replace(item,'mtAddLink("◧","PDF MENSUAL","Elegir año, mes y carpeta de destino",this::mtPdfMonthSelect);',1)
p.write_text(s)
print("V114: report menu provides year/month selection and direct PDF export to user-selected folder")
