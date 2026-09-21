package com.favorable.viajes;

import android.app.*; import android.os.*; import android.graphics.Color; import android.graphics.drawable.GradientDrawable;
import android.content.*; import android.view.*; import android.view.inputmethod.InputMethodManager; import android.widget.*;
import java.text.*; import java.util.*;

public class MainActivity extends Activity {
 final int BG=Color.rgb(8,13,10),PANEL=Color.rgb(20,29,23),PANEL2=Color.rgb(29,40,32),GREEN=Color.rgb(122,205,69),WHITE=Color.WHITE,MUTED=Color.rgb(177,190,181),RED=Color.rgb(218,70,70),YELLOW=Color.rgb(239,190,55);
 LinearLayout root,board; TextView weekTitle,foot; Calendar week=Calendar.getInstance(); SharedPreferences db;
 String[] days={"LUN","MAR","MIÉ","JUE","VIE","SÁB","DOM"};
 String[] companies={"ARCOR","BODEGA MONTEVIEJO","HOLCIM","CLIENTES VARIOS","EMPRESA / CLIENTE"};
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
  LinearLayout nav=new LinearLayout(this);String[] ns={"+ Viaje","Semana","★ Favoritos","Estadísticas"};
  for(String s:ns){Button x=bt(s);nav.addView(x,new LinearLayout.LayoutParams(0,64,1));if(s.startsWith("+"))x.setOnClickListener(v->form("",-1));if(s.startsWith("Est"))x.setOnClickListener(v->stats());}
  root.addView(nav);
  HorizontalScrollView hs=new HorizontalScrollView(this);hs.setFillViewport(false);ScrollView sv=new ScrollView(this);board=new LinearLayout(this);board.setOrientation(LinearLayout.VERTICAL);sv.addView(board);hs.addView(sv);root.addView(hs,new LinearLayout.LayoutParams(-1,0,1));
  foot=tx("",12,MUTED);root.addView(foot);
  p.setOnClickListener(v->{week.add(Calendar.WEEK_OF_YEAR,-1);render();});n.setOnClickListener(v->{week.add(Calendar.WEEK_OF_YEAR,1);render();});h.setOnClickListener(v->{week=Calendar.getInstance();render();});setContentView(root);render();
 }
 Calendar monday(){Calendar c=(Calendar)week.clone();int d=c.get(Calendar.DAY_OF_WEEK);c.add(Calendar.DATE,d==Calendar.SUNDAY?-6:Calendar.MONDAY-d);return c;}
 String wk(){return new SimpleDateFormat("yyyyMMdd",Locale.US).format(monday().getTime());}
 String key(int row,int day){return wk()+"_"+row+"_"+day;}
 void render(){
  Calendar c=monday(),e=(Calendar)c.clone();e.add(Calendar.DATE,6);SimpleDateFormat f=new SimpleDateFormat("dd/MM",new Locale("es","AR"));weekTitle.setText("SEMANA "+f.format(c.getTime())+" — "+f.format(e.getTime()));
  board.removeAllViews();LinearLayout hd=new LinearLayout(this);hd.addView(tx("EMPRESA",12,GREEN),new LinearLayout.LayoutParams(250,62));for(String d:days){TextView q=tx(d,12,GREEN);q.setGravity(Gravity.CENTER);hd.addView(q,new LinearLayout.LayoutParams(170,62));}board.addView(hd);
  int total=0,done=0,pending=0;
  for(int r=0;r<companies.length;r++){LinearLayout row=new LinearLayout(this);TextView cn=tx(companies[r],12,WHITE);cn.setBackground(shape(PANEL,12));row.addView(cn,new LinearLayout.LayoutParams(250,90));
   for(int d=0;d<7;d++){String val=db.getString(key(r,d),"");Button cell=bt(val.length()==0?"+":val);if(val.length()>0){cell.setTextColor(GREEN);total++;if(val.contains("REALIZADO"))done++;else pending++;}final int rr=r,dd=d;cell.setOnClickListener(v->{if(db.getString(key(rr,dd),"").isEmpty())form(companies[rr],dd);else tripMenu(rr,dd);});row.addView(cell,new LinearLayout.LayoutParams(170,90));}board.addView(row);
  }
  foot.setText("Viajes semana "+total+"   |   Realizados "+done+"   |   Pendientes "+pending+"   |   En curso 0   |   Reprogramados 0   |   Cancelados 0");
 }
 void form(String company,int day){
  ScrollView sc=new ScrollView(this);LinearLayout f=new LinearLayout(this);f.setOrientation(LinearLayout.VERTICAL);f.setPadding(28,8,28,8);sc.addView(f);
  EditText co=new EditText(this);co.setHint("Empresa / cliente");co.setText(company);f.addView(co);
  EditText tm=new EditText(this);tm.setHint("Hora · 08:30");f.addView(tm);
  Spinner ser=spin(new String[]{"RETIRO DE MATERIALES","SERVICIO DE RETIRO"});f.addView(label("Servicio"));f.addView(ser);
  Spinner drv=spin(drivers);f.addView(label("Chofer"));f.addView(drv);Spinner tr=spin(trucks);f.addView(label("Camión"));f.addView(tr);
  Spinner cont=spin(new String[]{"GDE 30 ROLL","MED 20 ROLL","CHICO 15 ROLL","GDE 18 PORTA","CHICO 8 PORTA"});f.addView(label("Contenedor"));f.addView(cont);
  EditText mat=new EditText(this);mat.setHint("Materiales: cartón, vidrio, PET...");f.addView(mat);EditText obs=new EditText(this);obs.setHint("Observaciones");f.addView(obs);
  int target=day<0?0:day;new AlertDialog.Builder(this).setTitle("Nuevo viaje · "+days[target]).setView(sc).setPositiveButton("GUARDAR",(x,y)->{int row=findCompany(co.getText().toString());String val=(tm.getText().length()>0?tm.getText()+" ":"")+ser.getSelectedItem().toString()+" · PROGRAMADO";db.edit().putString(key(row,target),val).apply();render();}).setNegativeButton("Cancelar",null).show();
 }
 TextView label(String s){TextView v=tx(s,11,MUTED);v.setTypeface(null,1);return v;}
 Spinner spin(String[] a){Spinner s=new Spinner(this);ArrayAdapter<String>x=new ArrayAdapter<String>(this,android.R.layout.simple_spinner_dropdown_item,a);s.setAdapter(x);return s;}
 int findCompany(String s){for(int i=0;i<companies.length;i++)if(companies[i].equalsIgnoreCase(s.trim()))return i;return companies.length-1;}
 void tripMenu(int r,int d){String v=db.getString(key(r,d),"");String[] a={"VER VIAJE","MARCAR REALIZADO","REPROGRAMAR","DUPLICAR","ELIMINAR"};new AlertDialog.Builder(this).setTitle(companies[r]+" · "+days[d]+"\n"+v).setItems(a,(x,w)->{if(w==0)new AlertDialog.Builder(this).setTitle("Ficha del viaje").setMessage(v).setPositiveButton("Cerrar",null).show();if(w==1){db.edit().putString(key(r,d),v.replace("PROGRAMADO","REALIZADO")).apply();render();}if(w==2)form(companies[r],d);if(w==3){int nd=(d+1)%7;db.edit().putString(key(r,nd),v).apply();render();}if(w==4){db.edit().remove(key(r,d)).apply();render();}}).show();}
 void stats(){int total=0;for(int r=0;r<companies.length;r++)for(int d=0;d<7;d++)if(!db.getString(key(r,d),"").isEmpty())total++;new AlertDialog.Builder(this).setTitle("Estadísticas").setMessage("Viajes de la semana: "+total+"\n\nPanel estadístico en construcción: empresa · estado · material · chofer · camión · destino.").setPositiveButton("Cerrar",null).show();}
}
