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
 Button alert=new Button(this);alert.setText("PROBAR ALERTA AL RELOJ");alert.setOnClickListener(v->WatchAlerts.testAlert(this));layout.addView(alert);
 TextView config=new TextView(this);config.setText("Opciones de grabación (se guardan; grabador pendiente)");layout.addView(config);
 Spinner quality=new Spinner(this);
 String[] resolutions={"480p","720p","1080p"};quality.setAdapter(new ArrayAdapter<String>(this,android.R.layout.simple_spinner_dropdown_item,resolutions));
 int savedResolution=RecordingPreferences.get(this).getInt("resolution",720);
 quality.setSelection(savedResolution==480?0:savedResolution==1080?2:1);layout.addView(quality);
 Spinner duration=new Spinner(this);String[] durations={"10 segundos","30 segundos","60 segundos"};
 duration.setAdapter(new ArrayAdapter<String>(this,android.R.layout.simple_spinner_dropdown_item,durations));
 int savedSeconds=RecordingPreferences.get(this).getInt("seconds",30);
 duration.setSelection(savedSeconds==10?0:savedSeconds==60?2:1);layout.addView(duration);
 CheckBox photos=new CheckBox(this);photos.setText("Fotos cada 5 segundos");photos.setChecked(RecordingPreferences.get(this).getBoolean("photos",true));layout.addView(photos);
 CheckBox audio=new CheckBox(this);audio.setText("Grabar audio");audio.setChecked(RecordingPreferences.get(this).getBoolean("audio",false));layout.addView(audio);
 Button save=new Button(this);save.setText("GUARDAR CONFIGURACIÓN");save.setOnClickListener(v->{
 int r=new int[]{480,720,1080}[quality.getSelectedItemPosition()];
 int sec=new int[]{10,30,60}[duration.getSelectedItemPosition()];
 RecordingPreferences.save(this,r,sec,photos.isChecked(),audio.isChecked());
 Toast.makeText(this,"Configuración guardada",Toast.LENGTH_SHORT).show();
 });layout.addView(save);
 Button record=new Button(this);record.setText("ABRIR CÁMARA Y GRABAR");record.setOnClickListener(v->startActivity(new android.content.Intent(this,RecorderActivity.class)));layout.addView(record);
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