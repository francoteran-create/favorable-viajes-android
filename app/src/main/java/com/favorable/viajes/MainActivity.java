package com.favorable.viajes;

import android.app.*;
import android.os.*;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.view.*;
import android.widget.*;
import java.text.*;
import java.util.*;

public class MainActivity extends Activity {
    final int BG=Color.rgb(11,15,12), PANEL=Color.rgb(24,31,26), GREEN=Color.rgb(121,201,67), WHITE=Color.WHITE, MUTED=Color.rgb(175,185,178);
    LinearLayout root, board; TextView weekTitle; Calendar week=Calendar.getInstance();
    String[] companies={"★ FAVORITOS","ARCOR","BODEGA MONTEVIEJO","HOLCIM","MENDOZA","CLIENTES VARIOS","EMPRESA / CLIENTE"};
    String[] days={"LUN","MAR","MIÉ","JUE","VIE","SÁB","DOM"};

    public void onCreate(Bundle b){super.onCreate(b); week.setFirstDayOfWeek(Calendar.MONDAY); build();}
    TextView t(String s,int sp,int c){TextView v=new TextView(this);v.setText(s);v.setTextSize(sp);v.setTextColor(c);v.setPadding(12,10,12,10);return v;}
    GradientDrawable bg(int c,float r){GradientDrawable g=new GradientDrawable();g.setColor(c);g.setCornerRadius(r);return g;}
    Button btn(String s){Button b=new Button(this);b.setText(s);b.setTextColor(WHITE);b.setTextSize(12);b.setBackground(bg(PANEL,12));return b;}
    void build(){
      root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setPadding(14,14,14,14);root.setBackgroundColor(BG);
      LinearLayout top=new LinearLayout(this);top.setGravity(Gravity.CENTER_VERTICAL);
      TextView brand=t("FAVORABLE  VIAJES",22,GREEN);brand.setTypeface(null,1);top.addView(brand,new LinearLayout.LayoutParams(0,-2,1));
      Button prev=btn("◀");Button today=btn("HOY");Button next=btn("▶"); top.addView(prev);top.addView(today);top.addView(next);root.addView(top);
      weekTitle=t("",15,WHITE);weekTitle.setGravity(Gravity.CENTER);root.addView(weekTitle);
      LinearLayout actions=new LinearLayout(this);String[] aa={"+ NUEVO VIAJE","VER SEMANA","★ FAVORITOS","ESTADÍSTICAS"};
      for(String a:aa){Button x=btn(a);actions.addView(x,new LinearLayout.LayoutParams(0,-2,1)); if(a.startsWith("+"))x.setOnClickListener(v->newTrip());}
      root.addView(actions);
      HorizontalScrollView hs=new HorizontalScrollView(this);ScrollView vs=new ScrollView(this);board=new LinearLayout(this);board.setOrientation(LinearLayout.VERTICAL);vs.addView(board);hs.addView(vs);root.addView(hs,new LinearLayout.LayoutParams(-1,0,1));
      TextView foot=t("Viajes semana  0   |   Realizados  0   |   En curso  0   |   Pendientes  0   |   Reprogramados  0   |   Cancelados  0",12,MUTED);root.addView(foot);
      prev.setOnClickListener(v->{week.add(Calendar.WEEK_OF_YEAR,-1);render();});next.setOnClickListener(v->{week.add(Calendar.WEEK_OF_YEAR,1);render();});today.setOnClickListener(v->{week=Calendar.getInstance();render();});
      setContentView(root);render();
    }
    void render(){
      Calendar c=(Calendar)week.clone();int d=c.get(Calendar.DAY_OF_WEEK);int delta=(d==Calendar.SUNDAY?-6:Calendar.MONDAY-d);c.add(Calendar.DATE,delta);
      SimpleDateFormat df=new SimpleDateFormat("dd/MM",new Locale("es","AR"));Calendar end=(Calendar)c.clone();end.add(Calendar.DATE,6);weekTitle.setText("SEMANA  "+df.format(c.getTime())+"  —  "+df.format(end.getTime()));
      board.removeAllViews();LinearLayout h=new LinearLayout(this);h.addView(t("EMPRESA",12,GREEN),new LinearLayout.LayoutParams(240,60));for(String day:days)h.addView(t(day,12,GREEN),new LinearLayout.LayoutParams(150,60));board.addView(h);
      for(String co:companies){LinearLayout r=new LinearLayout(this);TextView n=t(co,12,WHITE);n.setBackground(bg(PANEL,8));r.addView(n,new LinearLayout.LayoutParams(240,72));for(int i=0;i<7;i++){Button add=btn("+");final String cc=co,dd=days[i];add.setOnClickListener(v->newTripFor(cc,dd));r.addView(add,new LinearLayout.LayoutParams(150,72));}board.addView(r);}
    }
    void newTrip(){newTripFor("EMPRESA / CLIENTE","");}
    void newTripFor(String company,String day){
      LinearLayout f=new LinearLayout(this);f.setOrientation(LinearLayout.VERTICAL);f.setPadding(24,8,24,0);
      EditText co=new EditText(this);co.setHint("Empresa / cliente");co.setText(company.startsWith("★")?"":company);f.addView(co);
      EditText time=new EditText(this);time.setHint("Hora");f.addView(time);
      Spinner service=new Spinner(this);String[] ss={"RETIRO DE MATERIALES","SERVICIO DE RETIRO"};service.setAdapter(new ArrayAdapter<String>(this,android.R.layout.simple_spinner_dropdown_item,ss));f.addView(service);
      EditText obs=new EditText(this);obs.setHint("Observaciones");f.addView(obs);
      new AlertDialog.Builder(this).setTitle("NUEVO VIAJE "+day).setView(f).setPositiveButton("GUARDAR",(d,w)->Toast.makeText(this,"Viaje guardado para prueba",Toast.LENGTH_SHORT).show()).setNegativeButton("CANCELAR",null).show();
    }
}
