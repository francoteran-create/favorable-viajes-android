from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text(); mark=' void btn(String s,Runnable r){'; assert mark in s
code=r'''
 LinearLayout moreCard(String icon,String title,String sub,Runnable action){
  LinearLayout r=referenceRow(icon,title,sub,"›",Color.rgb(244,190,46));r.setOnClickListener(v->action.run());return r;
 }
 void exactMoreLive(){
  currentScreen="MAS";base("MÁS");body.addView(refHero("MÁS OPCIONES","Administración de Nautilus Country"));body.addView(moreCard("♙","Empleados","Gestionar personal",this::exactPersonList));body.addView(moreCard("◈","Sectores","Configurar sectores",this::employees));body.addView(moreCard("↻","Regímenes de turno","4x2, 2x2, 5x2, etc.",this::regimes));body.addView(moreCard("▥","Cobertura mínima","Definir requerimientos por sector",this::coverageSetup));body.addView(moreCard("⇩","Importar fichadas","Desde Attendance logs.xls",this::attendance));body.addView(moreCard("⛁","Backup / Restaurar","Copia de seguridad de datos",this::backup));body.addView(moreCard("⚙","Configuración","Tolerancias, horarios, sistema",this::regimes));body.addView(moreCard("i","Acerca de","Nautilus Country · Presentismo","",()->{}));exactBottom("MÁS");
 }
 LinearLayout moreCard(String icon,String title,String sub,String dummy,Runnable action){return moreCard(icon,title,sub,action);}
'''
s=s.replace(mark,code+"\n"+mark)
s=s.replace('else exactMore();','else exactMoreLive();')
s=s.replace('V35 REAL REPORTING','V36 MORE ACTIONS')
p.write_text(s);print("V36 more actions applied")
