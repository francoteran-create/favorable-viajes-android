from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' TextView homeTitle(String t){';assert mark in s
shell=r'''
 void masterShell(String title){
  LinearLayout root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setBackgroundResource(R.drawable.nautilus_home_bg);
  ScrollView scroll=new ScrollView(this);scroll.setFillViewport(true);
  body=new LinearLayout(this);body.setOrientation(LinearLayout.VERTICAL);body.setPadding(16,12,16,18);
  if(title!=null&&!title.isEmpty()){TextView h=homeTitle(title);h.setTextSize(22);body.addView(h);}
  scroll.addView(body,new ScrollView.LayoutParams(-1,-2));root.addView(scroll,new LinearLayout.LayoutParams(-1,0,1));
  LinearLayout nav=new LinearLayout(this);nav.setOrientation(LinearLayout.HORIZONTAL);nav.setPadding(4,4,4,4);
  String[] labs={"⌂\nINICIO","▣\nTURNOS","●\nPERSONAL","▥\nINFORMES","⚙\nCONFIG."};
  Runnable[] acts={this::masterImageHome,()->weekPlanner(new Date()),this::employees,this::quickReportHub,this::exactMoreLive};
  for(int i=0;i<labs.length;i++){TextView v=new TextView(this);v.setText(labs[i]);v.setTextColor(Color.WHITE);v.setTextSize(11);v.setGravity(Gravity.CENTER);v.setPadding(2,8,2,8);final int q=i;v.setOnClickListener(x->acts[q].run());nav.addView(v,new LinearLayout.LayoutParams(0,62,1));}
  root.addView(nav,new LinearLayout.LayoutParams(-1,70));setContentView(root);
 }
'''
s=s.replace(mark,shell+"\n"+mark)
# MASTER home must never call legacy base(), which was injecting the obsolete header/nav.
s=s.replace(' void masterImageHome(){\n  base("");',' void masterImageHome(){\n  masterShell("");')
# Weekly master screen also bypasses legacy shell.
s=s.replace(' void weekPlanner(Date focus){\n  base("TURNOS · SEMANA");\n  btn("⌂ INICIO",this::masterImageHome);',' void weekPlanner(Date focus){\n  masterShell("TURNOS · SEMANA");')
# Personnel hub: use master shell when entering the employee list.
s=s.replace(' void employees(){base("PERSONAL");',' void employees(){masterShell("PERSONAL");')
# Remove legacy in-body reference nav if any survived.
s=s.replace('  referenceNav();\n','')
p.write_text(s);print("V57 dedicated MASTER shell: legacy menus bypassed")
