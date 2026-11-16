package com.vigia.app;
import android.app.Activity;
import android.os.Bundle;
import android.widget.*;
import android.content.*;
public class MainActivity extends Activity {
 @Override public void onCreate(Bundle state) { super.onCreate(state);
 LinearLayout layout=new LinearLayout(this);layout.setOrientation(LinearLayout.VERTICAL);layout.setPadding(32,40,32,32);
 TextView title=new TextView(this);title.setText("VIGÍA — prueba de instalación");title.setTextSize(22);layout.addView(title);
 TextView status=new TextView(this);status.setText("Esta compilación comprueba instalación y arranque. Todavía NO graba ni vigila.");layout.addView(status);
 Button test=new Button(this);test.setText("COMPROBAR APLICACIÓN");test.setOnClickListener(v->Toast.makeText(this,"VIGÍA inicia correctamente",Toast.LENGTH_LONG).show());layout.addView(test);
 setContentView(layout);
 }
}