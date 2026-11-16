package com.vigia.app;
import android.Manifest;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.hardware.Camera;
import android.media.CamcorderProfile;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.SystemClock;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.widget.*;
import java.io.File;
import java.io.RandomAccessFile;

/** Visible manual recording prototype. Never records after the activity is paused. */
@SuppressWarnings("deprecation")
public class RecorderActivity extends Activity implements SurfaceHolder.Callback {
 private Camera camera;
 private MediaRecorder recorder;
 private SurfaceHolder holder;
 private TextView status;
 private boolean recording, surfaceReady, active;
 private int cameraId=-1;
 private File output, partial;
 private long deadline, segmentStart;
 private boolean segmented;
 private final Handler timer=new Handler(Looper.getMainLooper());
 private final Runnable check=new Runnable(){
  @Override public void run(){
   if(!recording)return;
   long now=SystemClock.elapsedRealtime();
   SafetyLimits.Mode mode=SafetyLimits.currentMode(RecorderActivity.this);
   if(mode==SafetyLimits.Mode.STOP_AND_FINALIZE){stopVideo("Límite crítico");return;}
   if(now>=deadline){stopVideo("Tiempo cumplido");return;}
   boolean warning=mode==SafetyLimits.Mode.SEGMENT_30_SECONDS;
   if(warning && ((!segmented && now-segmentStart>=2000) || now-segmentStart>=30000)){
    if(!finishFile("Segmento"))return;
    if(!active || !surfaceReady || SystemClock.elapsedRealtime()>=deadline)return;
    if(!startFile(false))return;
   }
   timer.postDelayed(this,1000);
  }
 };
 @Override public void onCreate(Bundle state){super.onCreate(state);
  LinearLayout root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);
  status=new TextView(this);status.setText("Grabación manual visible · sin audio");root.addView(status);
  SurfaceView preview=new SurfaceView(this);holder=preview.getHolder();holder.addCallback(this);
  root.addView(preview,new LinearLayout.LayoutParams(-1,0,1));
  Button start=new Button(this);start.setText("INICIAR VIDEO");start.setOnClickListener(v->startVideo());root.addView(start);
  Button stop=new Button(this);stop.setText("DETENER Y GUARDAR");stop.setOnClickListener(v->stopVideo("Detención manual"));root.addView(stop);
  setContentView(root);
  if(!allowed())requestPermissions(new String[]{Manifest.permission.CAMERA},7);
 }
 private boolean allowed(){return checkSelfPermission(Manifest.permission.CAMERA)==PackageManager.PERMISSION_GRANTED;}
 @Override public void onRequestPermissionsResult(int code,String[] permissions,int[] results){super.onRequestPermissionsResult(code,permissions,results);if(code==7&&allowed())openCamera();}
 private void openCamera(){
  if(camera!=null||!active||!allowed()||!surfaceReady||holder==null||!holder.getSurface().isValid())return;
  try{
   Camera.CameraInfo info=new Camera.CameraInfo();
   cameraId=-1;
   for(int i=0;i<Camera.getNumberOfCameras();i++){Camera.getCameraInfo(i,info);if(info.facing==Camera.CameraInfo.CAMERA_FACING_BACK){cameraId=i;break;}}
   if(cameraId<0)throw new IllegalStateException("No hay cámara trasera");
   camera=Camera.open(cameraId);
   Camera.Parameters params=camera.getParameters();
   if(params.getSupportedFlashModes()!=null&&params.getSupportedFlashModes().contains(Camera.Parameters.FLASH_MODE_OFF)){
    params.setFlashMode(Camera.Parameters.FLASH_MODE_OFF);camera.setParameters(params);
   }
   camera.setDisplayOrientation(90);camera.setPreviewDisplay(holder);camera.startPreview();
  }catch(Exception e){releaseCamera();status.setText("Error de cámara: "+e.getMessage());}
 }
 private void startVideo(){
  if(recording)return;
  if(!allowed()){requestPermissions(new String[]{Manifest.permission.CAMERA},7);return;}
  deadline=SystemClock.elapsedRealtime()+1000L*RecordingPreferences.get(this).getInt("seconds",30);
  if(startFile(true)){timer.removeCallbacks(check);timer.postDelayed(check,1000);}
 }
 private boolean startFile(boolean notify){
  if(!active||!surfaceReady)return false;
  SafetyLimits.Mode mode=SafetyLimits.currentMode(this);
  if(mode==SafetyLimits.Mode.STOP_AND_FINALIZE){status.setText("Batería o espacio insuficiente");return false;}
  openCamera();if(camera==null)return false;
  try{
   int height=RecordingPreferences.get(this).getInt("resolution",720);
   int quality=height==1080?CamcorderProfile.QUALITY_1080P:height==480?CamcorderProfile.QUALITY_480P:CamcorderProfile.QUALITY_720P;
   if(!CamcorderProfile.hasProfile(cameraId,quality)){status.setText("Resolución no compatible. Elegí otra.");return false;}
   CamcorderProfile profile=CamcorderProfile.get(cameraId,quality);
   camera.unlock();recorder=new MediaRecorder();recorder.setCamera(camera);
   recorder.setVideoSource(MediaRecorder.VideoSource.CAMERA);
   recorder.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4);
   recorder.setVideoEncoder(MediaRecorder.VideoEncoder.H264);
   recorder.setVideoSize(profile.videoFrameWidth,profile.videoFrameHeight);
   recorder.setVideoFrameRate(profile.videoFrameRate);
   recorder.setVideoEncodingBitRate(profile.videoBitRate);
   Camera.CameraInfo info=new Camera.CameraInfo();Camera.getCameraInfo(cameraId,info);
   recorder.setOrientationHint(info.orientation);
   output=MediaStorage.nextVideo(this);
   partial=new File(output.getParentFile(),output.getName()+".partial");
   recorder.setOutputFile(partial.getAbsolutePath());recorder.setPreviewDisplay(holder.getSurface());
   recorder.setOnErrorListener((r,what,extra)->{if(recording&&r==recorder)stopVideo("Error del grabador");});
   recorder.prepare();recorder.start();
   recording=true;segmentStart=SystemClock.elapsedRealtime();segmented=mode==SafetyLimits.Mode.SEGMENT_30_SECONDS;
   status.setText("Grabando "+profile.videoFrameHeight+"p"+(segmented?" · segmentos":""));
   if(notify)try{WatchAlerts.recordingStarted(this);}catch(RuntimeException ignored){}
   return true;
  }catch(Exception e){recording=false;releaseRecorder();releaseCamera();status.setText("No se pudo iniciar: "+e.getMessage());return false;}
 }
 private void stopVideo(String reason){
  timer.removeCallbacks(check);
  if(recording)finishFile(reason);
  if(active&&surfaceReady)openCamera();
 }
 private boolean finishFile(String reason){
  if(!recording)return false;
  boolean stopped=false;
  recording=false;
  try{recorder.stop();stopped=true;}catch(RuntimeException ignored){}
  finally{releaseRecorder();releaseCamera();}
  boolean saved=false;
  if(stopped&&partial!=null&&partial.length()>0){
   try(RandomAccessFile file=new RandomAccessFile(partial,"rw")){file.getFD().sync();}
   catch(Exception e){status.setText(reason+": archivo parcial conservado");return false;}
   saved=partial.renameTo(output);
  }
  status.setText(reason+(saved?" · Guardado: "+output.getName():" · Archivo parcial conservado"));
  return saved;
 }
 private void releaseRecorder(){if(recorder!=null){try{recorder.reset();}catch(Exception ignored){}try{recorder.release();}catch(Exception ignored){}recorder=null;}}
 private void releaseCamera(){if(camera!=null){try{camera.lock();}catch(Exception ignored){}try{camera.release();}catch(Exception ignored){}camera=null;}}
 @Override public void surfaceCreated(SurfaceHolder h){holder=h;surfaceReady=true;openCamera();}
 @Override public void surfaceChanged(SurfaceHolder h,int format,int width,int height){}
 @Override public void surfaceDestroyed(SurfaceHolder h){surfaceReady=false;stopVideo("Vista cerrada");releaseCamera();}
 @Override protected void onResume(){super.onResume();active=true;openCamera();}
 @Override protected void onPause(){active=false;stopVideo("Aplicación pausada");releaseCamera();super.onPause();}
 @Override protected void onDestroy(){active=false;stopVideo("Aplicación cerrada");releaseCamera();super.onDestroy();}
}
