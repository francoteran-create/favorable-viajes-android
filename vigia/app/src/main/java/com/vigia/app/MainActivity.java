package com.vigia.app;
import android.app.Activity;
import android.os.Bundle;
import android.content.Context;
import android.hardware.*;
import android.widget.*;
import java.util.Locale;
public class MainActivity extends Activity implements SensorEventListener {
 private SensorManager sensors;
 private Sensor accel,light;
 private TextView status;
 private boolean monitoring=false;
 private float lastLux=-1;
 private long lastEvent=0;
 @Override public void onCreate(Bundle state) {super.onCreate(state);
 sensors=(SensorManager)getSystemService(Context.SENSOR_SERVICE);
 accel=sensors.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
 light=sensors.getDefaultSensor(Sensor.TYPE_LIGHT);
 LinearLayout layout=new LinearLayout(this);layout.setOrientation(LinearLayout.VERTICAL);layout.setPadding(32,40,32,32);
 TextView title=new TextView(this);title.setText("VIGÍA — prueba de sensores");title.setTextSize(22);layout.addView(title);
 status=new TextView(this);status.setText("Sensores detenidos. Esta versión NO graba video.");layout.addView(status);
 Button start=new Button(this);start.setText("INICIAR SENSORES");start.setOnClickListener(v->startSensors());layout.addView(start);
 Button stop=new Button(this);stop.setText("DETENER");stop.setOnClickListener(v->stopSensors());layout.addView(stop);
 setContentView(layout);
 }
 private void startSensors(){if(monitoring)return;monitoring=true;lastLux=-1;
 if(accel!=null)sensors.registerListener(this,accel,SensorManager.SENSOR_DELAY_NORMAL);
 if(light!=null)sensors.registerListener(this,light,SensorManager.SENSOR_DELAY_NORMAL);
 status.setText("Sensores activos. No hay grabación ni vigilancia con pantalla apagada.");}
 private void stopSensors(){monitoring=false;sensors.unregisterListener(this);status.setText("Sensores detenidos.");}
 @Override public void onSensorChanged(SensorEvent event){if(!monitoring)return;
 long now=android.os.SystemClock.elapsedRealtime();if(now-lastEvent<1500)return;
 if(event.sensor.getType()==Sensor.TYPE_LIGHT){float lux=event.values[0];
 if(lastLux>=0&&Math.abs(lux-lastLux)>Math.max(25f,lastLux*0.35f)){lastEvent=now;status.setText(String.format(Locale.US,"Cambio de luz: %.0f lux",lux));}
 lastLux=lux;
 }else if(event.sensor.getType()==Sensor.TYPE_ACCELEROMETER){
 float x=event.values[0],y=event.values[1],z=event.values[2];
 float deviation=Math.abs((float)Math.sqrt(x*x+y*y+z*z)-9.81f);
 if(deviation>3.5f){lastEvent=now;status.setText("Movimiento físico detectado");}
 }}
 @Override public void onAccuracyChanged(Sensor sensor,int accuracy){}
 @Override protected void onPause(){super.onPause();stopSensors();}
 @Override protected void onDestroy(){stopSensors();super.onDestroy();}
}