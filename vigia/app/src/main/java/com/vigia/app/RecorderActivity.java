package com.vigia.app;
import android.Manifest;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.hardware.Camera;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import java.io.File;
/** Foreground-only manual recording prototype; not background surveillance. */
@SuppressWarnings("deprecation")
public class RecorderActivity extends Activity implements SurfaceHolder.Callback {
 private Camera camera;
 private MediaRecorder recorder;
 private SurfaceHolder holder;
 private TextView status;
 private boolean recording=false;
 private File output;
 private boolean surfaceReady=false;
 private final android.os.Handler timer=new android.os.Handler(android.os.Looper.getMainLooper());
 private final Runnable timeout=()->{if(recording)stopVideo();};
 private final Runnable check=new Runnable(){@Override public void run(){if(!recording)return;
  if(SafetyLimits.currentMode(RecorderActivity.this)==SafetyLimits.Mode.STOP_AND_FINALIZE){stopVideo();status.setText("Grabación detenida por batería o espacio crítico");return;}
  timer.postDelayed(this,2000);
 }};
 @Override public void onCreate(Bundle state){super.onCreate(state);
  LinearLayout root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);
  status=new TextView(this);status.setText("Esperando cámara");root.addView(status);
  SurfaceView preview=new SurfaceView(this);holder=preview.getHolder();holder.addCallback(this);
  root.addView(preview,new LinearLayout.LayoutParams(-1,0,1));
  Button start=new Button(this);start.setText("INICIAR VIDEO");start.setOnClickListener(v->startVideo());root.addView(start);
  Button stop=new Button(this);stop.setText("DETENER Y GUARDAR");stop.setOnClickListener(v->stopVideo());root.addView(stop);
  setContentView(root);
  if(checkSelfPermission(Manifest.permission.CAMERA)!=PackageManager.PERMISSION_GRANTED)requestPermissions(new String[]{Manifest.permission.CAMERA},7);
 }
 @Override public void onRequestPermissionsResult(int requestCode,String[] permissions,int[] results){super.onRequestPermissionsResult(requestCode,permissions,results);if(requestCode==7&&results.length>0&&results[0]==PackageManager.PERMISSION_GRANTED)openCamera();}
 private void openCamera(){if(camera!=null||holder==null||!surfaceReady||!holder.getSurface().isValid())return;
  try{camera=Camera.open();camera.setDisplayOrientation(90);camera.setPreviewDisplay(holder);camera.startPreview();status.setText("Cámara lista");}
  catch(Exception e){status.setText("Error de cámara: "+e.getMessage());releaseCamera();}
 }
 private void startVideo(){if(recording)return;
  if(checkSelfPermission(Manifest.permission.CAMERA)!=PackageManager.PERMISSION_GRANTED){status.setText("Permiso de cámara requerido");return;}
  if(camera==null){openCamera();if(camera==null)return;}
  if(!surfaceReady){status.setText("Vista previa no disponible");return;}
  if(SafetyLimits.currentMode(this)==SafetyLimits.Mode.STOP_AND_FINALIZE){status.setText("Batería o almacenamiento insuficiente");return;}
  try{
   camera.stopPreview();camera.unlock();recorder=new MediaRecorder();recorder.setCamera(camera);
   recorder.setVideoSource(MediaRecorder.VideoSource.CAMERA);
   recorder.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4);
   recorder.setVideoEncoder(MediaRecorder.VideoEncoder.H264);
   recorder.setVideoSize(640,480);recorder.setVideoFrameRate(24);recorder.setVideoEncodingBitRate(1500000);
   output=MediaStorage.nextVideo(this);recorder.setOutputFile(output.getAbsolutePath());
   recorder.setPreviewDisplay(holder.getSurface());recorder.prepare();recorder.start();
   recording=true;status.setText("Grabando: "+output.getName());WatchAlerts.recordingStarted(this);
   timer.postDelayed(check,2000);
   int duration=RecordingPreferences.get(this).getInt("seconds",30);
   timer.postDelayed(timeout,duration*1000L);
  }catch(Exception e){status.setText("No se pudo iniciar: "+e.getMessage());releaseRecorder();openCamera();}
 }
 private void stopVideo(){if(!recording)return;timer.removeCallbacks(check);timer.removeCallbacks(timeout);boolean saved=false;
  try{recorder.stop();saved=true;}catch(RuntimeException e){status.setText("Grabación incompleta");}
  finally{recording=false;releaseRecorder();}
  if(!saved&&output!=null)output.delete();
  if(saved&&output!=null)status.setText("Guardado: "+output.getName());
  if(surfaceReady)openCamera();
 }
 private void releaseRecorder(){if(recorder!=null){try{recorder.reset();recorder.release();}catch(Exception ignored){}recorder=null;}releaseCamera();}
 private void releaseCamera(){if(camera!=null){try{camera.lock();camera.release();}catch(Exception ignored){}camera=null;}}
 @Override public void surfaceCreated(SurfaceHolder h){holder=h;surfaceReady=true;if(checkSelfPermission(Manifest.permission.CAMERA)==PackageManager.PERMISSION_GRANTED)openCamera();}
 @Override public void surfaceChanged(SurfaceHolder h,int format,int width,int height){}
 @Override public void surfaceDestroyed(SurfaceHolder h){surfaceReady=false;stopVideo();releaseCamera();}
 @Override protected void onPause(){stopVideo();releaseCamera();super.onPause();}
 @Override protected void onDestroy(){stopVideo();releaseCamera();super.onDestroy();}
}