package com.favorable.viajes;

import android.app.*; import android.os.*; import android.graphics.Color; import android.graphics.drawable.GradientDrawable;
import android.content.*; import android.view.*; import android.view.inputmethod.InputMethodManager; import android.widget.*;
import java.text.*; import java.util.*;

public class MainActivity extends Activity {
 final int BG=Color.rgb(8,13,10),PANEL=Color.rgb(20,29,23),PANEL2=Color.rgb(29,40,32),GREEN=Color.rgb(122,205,69),WHITE=Color.WHITE,MUTED=Color.rgb(177,190,181),RED=Color.rgb(218,70,70),YELLOW=Color.rgb(239,190,55);
 LinearLayout root,board; TextView weekTitle,foot; Calendar week=Calendar.getInstance(); SharedPreferences db;
 String[] days={"LUN","MAR","MIÉ","JUE","VIE","SÁB","DOM"};
 String[] companies={"ARCOR","BODEGA MONTEVIEJO","HOLCIM","CLIENTES VARIOS","EMPRESA / CLIENTE"};
 boolean favoritesOnly=false;
 String[] trailers={"SIN ACOPLADO","AE 056 WL · ACOPLADO","CMC 802 · ACOPLADO","TCM 673 · ACOPLADO","TDH 077 · ACOPLADO"};
 String[] materials={"CARTON","VIDRIO","STRECH","TERMOCONTRAIBLE","ALUMINIO","CHATARRA","PET CRISTAL","BIDONES","COLOR"};
 String[] destinations={"RELLENO SANITARIO","HOLCIM","FAVORABLE","OTRO"};
 String[] states={"PEDIDO PENDIENTE","PROGRAMADO","EN CURSO","REALIZADO","REPROGRAMADO","CANCELADO"};
 String[] drivers={"AGUERO EDGARDO JESUS","CATALDO DANIEL HECTOR","CATALDO FRANCO","CATALDO SERGIO JAVIER","FUNES FABIAN ROQUE","GINIOLI MATIAS VICENTE","MELA GERARDO DARIO","OLMOS JUAN CARLOS","SOTELO FRANCO"};
 String[] trucks={"AC 592 VP · IVECO EUROCARGO","AG 824 DR · IVECO TECTOR","AD 604 WN · IVECO DAILY","AD 670 RD · IVECO TECTOR","AE 056 WX · IVECO TECTOR","AF 252 GE · IVECO TECTOR","DOJ 270 · M. BENZ LK","GIP 868 · M. BENZ L","ILH 135 · IVECO DAILY","OIN 428 · FORD CARGO","PQJ 269 · IVECO EUROCARGO","DPI439 · M. BENZ LK","AI 375 JY · IVECO TECTOR"};
 public void onCreate(Bundle b){super.onCreate(b);db=getSharedPreferences("viajes",0);build();}
 TextView tx(String s,int z,int c){TextView v=new TextView(this);v.setText(s);v.setTextSize(z);v.setTextColor(c);v.setPadding(14,10,14,10);return v;}
 GradientDrawable shape(int c,float r){GradientDrawable g=new GradientDrawable();g.setColor(c);g.setCornerRadius(r);return g;}
 Button bt(String s){Button b=new Button(this);b.setText(s);b.setTextColor(WHITE);b.setTextSize(11);b.setAllCaps(false);b.setBackground(shape(PANEL2,16));return b;}
 void build(){
  root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setPadding(12,10,12,8);root.setBackgroundColor(BG);
  LinearLayout top=new LinearLayout(this);top.setGravity(Gravity.CENTER_VERTICAL);TextView brand=tx("FAVORABLE\nVIAJES",22,GREEN);brand.setTypeface(null,1);top.addView(brand,new LinearLayout.LayoutParams(0,-2,1));
  Button p=bt("‹"),h=bt("HOY"),n=bt("›");top.addView(p);top.addView(h);top.addView(n);root.addView(top);
  weekTitle=tx("",16,WHITE);weekTitle.setGravity(Gravity.CENTER);weekTitle.setTypeface(null,1);root.addView(weekTitle);
  LinearLayout nav=new LinearLayout(this);String[] ns={"+ Viaje","Semana","★ Favoritos","Estadísticas","Historial"};
  for(String s:ns){Button x=bt(s);nav.addView(x,new LinearLayout.LayoutParams(0,64,1));if(s.startsWith("+"))x.setOnClickListener(v->form("",-1));if(s.startsWith("Est"))x.setOnClickListener(v->stats());if(s.contains("Favoritos"))x.setOnClickListener(v->{favoritesOnly=!favoritesOnly;render();});if(s.equals("Historial"))x.setOnClickListener(v->history());}
  root.addView(nav);
  HorizontalScrollView hs=new HorizontalScrollView(this);hs.setFillViewport(false);ScrollView sv=new ScrollView(this);board=new LinearLayout(this);board.setOrientation(LinearLayout.VERTICAL);sv.addView(board);hs.addView(sv);root.addView(hs,new LinearLayout.LayoutParams(-1,0,1));
  foot=tx("",12,MUTED);root.addView(foot);
  p.setOnClickListener(v->{week.add(Calendar.WEEK_OF_YEAR,-1);render();});n.setOnClickListener(v->{week.add(Calendar.WEEK_OF_YEAR,1);render();});h.setOnClickListener(v->{week=Calendar.getInstance();render();});setContentView(root);render();
 }
 Calendar monday(){Calendar c=(Calendar)week.clone();int d=c.get(Calendar.DAY_OF_WEEK);c.add(Calendar.DATE,d==Calendar.SUNDAY?-6:Calendar.MONDAY-d);return c;}
 String wk(){return new SimpleDateFormat("yyyyMMdd",Locale.US).format(monday().getTime());}
 String key(int row,int day){return wk()+"_"+row+"_"+day;}
 String[] trips(int row,int day){String raw=db.getString(key(row,day),"");return raw.length()==0?new String[0]:raw.split("\\|\\|",-1);}
 String summary(int row,int day){String[] a=trips(row,day);if(a.length==0)return "+";StringBuilder z=new StringBuilder();for(int i=0;i<a.length;i++){if(i>0)z.append("\n");z.append(i+1).append(" · ").append(a[i]);}return z.toString();}
 void appendTrip(int row,int day,String v){String k=key(row,day),old=db.getString(k,"");db.edit().putString(k,old.length()==0?v:old+"||"+v).apply();}
 void saveHistory(String action,String detail){String old=db.getString("history","");String now=new SimpleDateFormat("dd/MM HH:mm",new Locale("es","AR")).format(new Date());db.edit().putString("history",now+" · "+action+" · "+detail+"\n"+old).apply();}
 void render(){
  Calendar c=monday(),e=(Calendar)c.clone();e.add(Calendar.DATE,6);SimpleDateFormat f=new SimpleDateFormat("dd/MM",new Locale("es","AR"));weekTitle.setText("SEMANA "+f.format(c.getTime())+" — "+f.format(e.getTime()));
  board.removeAllViews();LinearLayout hd=new LinearLayout(this);hd.addView(tx("EMPRESA",12,GREEN),new LinearLayout.LayoutParams(250,62));for(String d:days){TextView q=tx(d,12,GREEN);q.setGravity(Gravity.CENTER);hd.addView(q,new LinearLayout.LayoutParams(170,62));}board.addView(hd);
  int total=0,done=0,pending=0;
  for(int r=0;r<companies.length;r++){if(favoritesOnly&&!db.getBoolean("fav_"+r,false))continue;LinearLayout row=new LinearLayout(this);TextView cn=tx(companies[r],12,WHITE);cn.setBackground(shape(PANEL,12));final int fr=r;cn.setOnLongClickListener(v->{boolean nv=!db.getBoolean("fav_"+fr,false);db.edit().putBoolean("fav_"+fr,nv).apply();Toast.makeText(this,nv?"Agregado a favoritos":"Quitado de favoritos",Toast.LENGTH_SHORT).show();render();return true;});if(db.getBoolean("fav_"+r,false))cn.setText("★ "+companies[r]);row.addView(cn,new LinearLayout.LayoutParams(250,90));
   for(int d=0;d<7;d++){String val=db.getString(key(r,d),"");Button cell=bt(summary(r,d));if(val.length()>0){cell.setTextColor(GREEN);String[] ta=trips(r,d);total+=ta.length;for(String tv:ta){if(tv.contains("REALIZADO"))done++;else pending++;}}final int rr=r,dd=d;cell.setOnClickListener(v->{if(db.getString(key(rr,dd),"").isEmpty())form(companies[rr],dd);else tripMenu(rr,dd);});row.addView(cell,new LinearLayout.LayoutParams(170,90));}board.addView(row);
  }
  foot.setText("Viajes semana "+total+"   |   Realizados "+done+"   |   Pendientes "+pending+"   |   En curso 0   |   Reprogramados 0   |   Cancelados 0");
 }
 void form(String company,int day){
  ScrollView sc=new ScrollView(this);LinearLayout f=new LinearLayout(this);f.setOrientation(LinearLayout.VERTICAL);f.setPadding(28,8,28,8);sc.addView(f);
  EditText co=new EditText(this);co.setHint("Empresa / cliente");co.setText(company);f.addView(co);
  EditText tm=new EditText(this);tm.setHint("Hora · 08:30");f.addView(tm);
  Spinner ser=spin(new String[]{"RETIRO DE MATERIALES","SERVICIO DE RETIRO"});f.addView(label("Servicio"));f.addView(ser);
  Spinner drv=spin(drivers);f.addView(label("Chofer"));f.addView(drv);Spinner tr=spin(trucks);f.addView(label("Camión"));f.addView(tr);
  Spinner trail=spin(trailers);f.addView(label("Acoplado"));f.addView(trail);
  Spinner cont=spin(new String[]{"GDE 30 ROLL","MED 20 ROLL","CHICO 15 ROLL","GDE 18 PORTA","CHICO 8 PORTA"});f.addView(label("Contenedor"));f.addView(cont);
  Spinner dest=spin(destinations);f.addView(label("Destino / disposición"));f.addView(dest);
  Spinner st=spin(states);st.setSelection(1);f.addView(label("Estado"));f.addView(st);
  TextView mat=tx("Seleccionar materiales",13,GREEN);mat.setBackground(shape(PANEL2,12));final boolean[] sel=new boolean[materials.length];final String[] chosen={""};mat.setOnClickListener(v->new AlertDialog.Builder(this).setTitle("Materiales").setMultiChoiceItems(materials,sel,(a,i,on)->sel[i]=on).setPositiveButton("ACEPTAR",(a,b)->{StringBuilder z=new StringBuilder();for(int i=0;i<materials.length;i++)if(sel[i]){if(z.length()>0)z.append(", ");z.append(materials[i]);}chosen[0]=z.toString();mat.setText(chosen[0].length()==0?"Seleccionar materiales":chosen[0]);}).show());f.addView(label("Materiales"));f.addView(mat);EditText obs=new EditText(this);obs.setHint("Observaciones");f.addView(obs);
  int target=day<0?0:day;new AlertDialog.Builder(this).setTitle("Nuevo viaje · "+days[target]).setView(sc).setPositiveButton("GUARDAR",(x,y)->{int row=findCompany(co.getText().toString());String val=(tm.getText().length()>0?tm.getText()+" ":"")+ser.getSelectedItem().toString()+(chosen[0].length()>0?" · "+chosen[0]:"")+" · "+st.getSelectedItem().toString();appendTrip(row,target,val);saveHistory("ALTA",companies[row]+" · "+days[target]+" · "+val);render();}).setNegativeButton("Cancelar",null).show();
 }
 TextView label(String s){TextView v=tx(s,11,MUTED);v.setTypeface(null,1);return v;}
 Spinner spin(String[] a){Spinner s=new Spinner(this);ArrayAdapter<String>x=new ArrayAdapter<String>(this,android.R.layout.simple_spinner_dropdown_item,a);s.setAdapter(x);return s;}
 int findCompany(String s){for(int i=0;i<companies.length;i++)if(companies[i].equalsIgnoreCase(s.trim()))return i;return companies.length-1;}
 void tripMenu(int r,int d){String[] list=trips(r,d);if(list.length>1){String[] names=new String[list.length];for(int i=0;i<list.length;i++)names[i]=(i+1)+" · "+list[i];new AlertDialog.Builder(this).setTitle(companies[r]+" · "+days[d]+" · VIAJES").setItems(names,(a,i)->tripActions(r,d,i)).setNegativeButton("+ NUEVO VIAJE",(a,b)->form(companies[r],d)).show();return;}tripActions(r,d,0);}
 void tripActions(int r,int d,int idx){String[] list=trips(r,d);if(list.length==0)return;String v=list[idx];String[] a={"VER VIAJE","CAMBIAR ESTADO","EDITAR / REPROGRAMAR","DUPLICAR","CANCELAR VIAJE"};new AlertDialog.Builder(this).setTitle(companies[r]+" · "+days[d]+"\n"+v).setItems(a,(x,w)->{if(w==0)new AlertDialog.Builder(this).setTitle("Ficha del viaje · "+companies[r]+" · "+days[d]).setMessage("SEMANA: "+weekTitle.getText()+"\n\n"+v+"\n\nToque CAMBIAR ESTADO para avanzar el viaje.\nMantenga pulsada una empresa para marcarla favorita.").setPositiveButton("Cerrar",null).show();if(w==1)stateDialog(r,d,idx,v);if(w==2)form(companies[r],d);if(w==3){int nd=(d+1)%7;appendTrip(r,nd,v);saveHistory("DUPLICADO",companies[r]+" · "+days[d]+" → "+days[nd]);render();}if(w==4){replaceTrip(r,d,idx,v.replace("PROGRAMADO","CANCELADO").replace("EN CURSO","CANCELADO").replace("PEDIDO PENDIENTE","CANCELADO"));saveHistory("CANCELADO",companies[r]+" · "+days[d]);render();}}).show();}
 void replaceTrip(int r,int d,int idx,String nv){String[] a=trips(r,d);if(idx<0||idx>=a.length)return;a[idx]=nv;StringBuilder z=new StringBuilder();for(int i=0;i<a.length;i++){if(i>0)z.append("||");z.append(a[i]);}db.edit().putString(key(r,d),z.toString()).apply();}
 void stateDialog(int r,int d,int idx,String v){new AlertDialog.Builder(this).setTitle("Cambiar estado").setItems(states,(x,i)->{String nv=v;for(String z:states)nv=nv.replace(z,states[i]);replaceTrip(r,d,idx,nv);saveHistory("ESTADO",companies[r]+" · "+states[i]);render();}).show();}
 void history(){String h=db.getString("history","Sin movimientos todavía.");ScrollView sc=new ScrollView(this);TextView v=tx(h,13,WHITE);v.setBackgroundColor(BG);sc.addView(v);new AlertDialog.Builder(this).setTitle("Historial / trazabilidad").setView(sc).setPositiveButton("Cerrar",null).show();}
 void stats(){int total=0;for(int r=0;r<companies.length;r++)for(int d=0;d<7;d++)if(!db.getString(key(r,d),"").isEmpty())total++;new AlertDialog.Builder(this).setTitle("Estadísticas").setMessage("Viajes de la semana: "+total+"\n\nPanel estadístico en construcción: empresa · estado · material · chofer · camión · destino.").setPositiveButton("Cerrar",null).show();}
}
