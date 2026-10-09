from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' void mtPersonnel(){'
assert mark in s
extra=r'''
 void mtDayRoster(String day){
  currentScreen="DIA";mtScreen("DIAGRAMA DEL DÍA",1);
  TextView date=mtText(day,16,mtPale(),true);date.setPadding(mtDp(7),0,0,mtDp(12));body.addView(date);
  boolean imported=evaluatedThrough(day)==1;
  TextView mode=mtText(imported?"FICHADAS IMPORTADAS · VERIFICAR INCIDENCIAS":"PROGRAMADO · FICHADAS PENDIENTES DE IMPORTAR",11,imported?Color.rgb(82,220,161):mtGold(),true);mode.setPadding(mtDp(8),mtDp(7),mtDp(8),mtDp(12));body.addView(mode);
  Cursor cursor=null;int people=0,scheduled=0;
  try{
   cursor=db.getReadableDatabase().rawQuery("SELECT p.id,p.name,coalesce(s.name,'SIN SECTOR') FROM people p LEFT JOIN sectors s ON s.id=p.sector_id WHERE p.active=1 ORDER BY p.name",null);
   while(cursor.moveToNext()){
    String id=cursor.getString(0),name=cursor.getString(1),sector=cursor.getString(2);people++;
    DayResult result=calcDay(id,day);if(result==null||!result.expected)continue;scheduled++;
    String status=!imported?"PROGRAMADO · AÚN SIN IMPORTAR":result.worked>0?(result.late>0?"TARDANZA "+result.late+" MIN":"JORNADA REGISTRADA"):"SIN FICHADAS · REVISAR";
    mtAddLink("●",name,sector+" · "+status,()->mtEmployee(id));
   }
  }catch(Exception e){body.addView(mtText("No se pudo cargar el diagrama: "+e.getMessage(),12,mtPale(),false));}
  finally{if(cursor!=null)cursor.close();}
  if(scheduled==0)body.addView(mtText(people==0?"Todavía no hay personal. Agregalo desde PERSONAL.":"No hay empleados diagramados para esta fecha.",14,mtPale(),false));
  mtAddLink("▣","VOLVER A LA SEMANA","Ver todos los días",()->mtWeek(parseDate(day)));
 }
 void mtEmployee(String pid){
  currentScreen="FICHA";mtScreen("FICHA DEL PERSONAL",2);
  String[] a=personMaster(pid);
  LinearLayout panel=mtPanel();panel.setGravity(Gravity.CENTER_HORIZONTAL);
  ImageView photo=new ImageView(this);photo.setScaleType(ImageView.ScaleType.CENTER_CROP);
  String uri=a.length>11?a[11]:"";
  if(uri!=null&&!uri.trim().isEmpty()){
   try{photo.setImageURI(android.net.Uri.parse(uri));}catch(Exception e){photo.setImageResource(android.R.drawable.ic_menu_camera);}
  }else photo.setImageResource(android.R.drawable.ic_menu_camera);
  photo.setBackground(mtBg(0xFF0D3043,0xFF041321,mtGold(),64));
  photo.setContentDescription("Fotografía · tocar para agregar o cambiar");
  photo.setOnClickListener(v->pickEmployeePhoto(pid));
  LinearLayout.LayoutParams pl=new LinearLayout.LayoutParams(mtDp(132),mtDp(132));pl.bottomMargin=mtDp(8);panel.addView(photo,pl);
  TextView name=mtText(a[0].isEmpty()?"Empleado "+pid:a[0],21,Color.WHITE,true);name.setGravity(Gravity.CENTER);panel.addView(name,new LinearLayout.LayoutParams(-1,-2));
  TextView sector=mtText(a[1].isEmpty()?"Sector por configurar":a[1],13,mtPale(),false);sector.setGravity(Gravity.CENTER);
  panel.addView(sector,new LinearLayout.LayoutParams(-1,mtDp(25)));
  TextView prompt=mtText(uri==null||uri.isEmpty()?"TOCAR LA IMAGEN PARA AGREGAR FOTO":"TOCAR LA IMAGEN PARA CAMBIAR FOTO",11,mtGold(),true);prompt.setGravity(Gravity.CENTER);
  panel.addView(prompt,new LinearLayout.LayoutParams(-1,mtDp(23)));
  body.addView(panel,new LinearLayout.LayoutParams(-1,-2));
  mtAddLink("✎","EDITAR FICHA COMPLETA","DNI, CUIL, ingreso, horario y sector",()->personnelMasterForm(pid));
  mtAddLink("▧","CAMBIAR FOTO","Elegir fotografía de la galería",()->pickEmployeePhoto(pid));
  mtAddLink("▣","VER DIAGRAMA","Planificación de turnos del personal",()->exactEmployeeMonth(pid));
  String[] labels={"DNI","CUIL","TELÉFONO","DOMICILIO","FECHA DE INGRESO","FUNCIÓN"};
  int[] idx={3,4,5,6,8,9};
  for(int i=0;i<labels.length;i++){if(a.length>idx[i]&&a[idx[i]]!=null&&!a[idx[i]].isEmpty()){
   TextView t=mtText(labels[i]+"  ·  "+a[idx[i]],13,mtPale(),false);t.setPadding(mtDp(10),mtDp(5),mtDp(4),mtDp(5));body.addView(t);
  }}
 }
'''
s=s.replace(mark,extra+"\n"+mark,1)
# Keep all V59 daily/employee pathways within the new styled navigation.
s=s.replace('v->exactDayRoster(ds)','v->mtDayRoster(ds)')
s=s.replace('()->exactDayRoster(ds)','()->mtDayRoster(ds)')
s=s.replace('()->exactPersonal(id)','()->mtEmployee(id)')
# Photo picker completion should return to the new profile, not obsolete legacy form.
s=s.replace('notice("Foto guardada");personnelMasterForm(p);','notice("Foto guardada");mtEmployee(p);')
p.write_text(s)
print("V61 native day roster and photo-enabled employee profile")
