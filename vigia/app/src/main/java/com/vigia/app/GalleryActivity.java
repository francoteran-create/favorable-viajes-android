package com.vigia.app;

import android.app.Activity;
import android.app.AlertDialog;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.view.ViewGroup;
import android.widget.*;
import java.io.File;
import java.text.DateFormat;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Date;
import java.util.Locale;

/** Local, visible media browser. Does not record or send media. */
public class GalleryActivity extends Activity {
 private LinearLayout root, list;
 private VideoView player;
 private ImageView image;
 private TextView info;
 private File selected;
 @Override public void onCreate(Bundle state){
  super.onCreate(state);
  root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setPadding(16,24,16,16);
  TextView title=new TextView(this);title.setText("Grabaciones");title.setTextSize(22);root.addView(title);
  info=new TextView(this);root.addView(info);
  player=new VideoView(this);root.addView(player,new LinearLayout.LayoutParams(-1,0,1));player.setVisibility(android.view.View.GONE);
  MediaController controller=new MediaController(this);controller.setAnchorView(player);player.setMediaController(controller);
  player.setOnErrorListener((mp,what,extra)->{info.setText("No se pudo reproducir este archivo.");return true;});
  image=new ImageView(this);image.setAdjustViewBounds(true);image.setScaleType(ImageView.ScaleType.FIT_CENTER);
  root.addView(image,new LinearLayout.LayoutParams(-1,0,1));image.setVisibility(android.view.View.GONE);
  Button refresh=new Button(this);refresh.setText("ACTUALIZAR LISTA");refresh.setOnClickListener(v->refresh());root.addView(refresh);
  Button delete=new Button(this);delete.setText("ELIMINAR ARCHIVO SELECCIONADO");delete.setOnClickListener(v->confirmDelete());root.addView(delete);
  ScrollView scroll=new ScrollView(this);list=new LinearLayout(this);list.setOrientation(LinearLayout.VERTICAL);scroll.addView(list);root.addView(scroll,new LinearLayout.LayoutParams(-1,0,1));
  setContentView(root);refresh();
 }
 private void addFiles(ArrayList<File> out,File folder){
  File[] files=folder.listFiles();if(files==null)return;
  for(File f:files){String n=f.getName().toLowerCase(Locale.ROOT);if(f.isFile()&&(n.endsWith(".mp4")||n.endsWith(".jpg")||n.endsWith(".jpeg")||n.endsWith(".partial")))out.add(f);}
 }
 private void refresh(){
  clearSelection();list.removeAllViews();
  ArrayList<File> files=new ArrayList<>();
  try{addFiles(files,MediaStorage.videos(this));addFiles(files,MediaStorage.photos(this));}catch(RuntimeException e){info.setText("No se puede leer el almacenamiento.");return;}
  files.sort(Comparator.comparingLong(File::lastModified).reversed());
  info.setText(files.isEmpty()?"No hay grabaciones guardadas.":files.size()+" archivos · elegí uno");
  for(File f:files){
   Button item=new Button(this);item.setAllCaps(false);
   String type=f.getName().endsWith(".partial")?"Parcial":f.getName().endsWith(".mp4")?"Video":"Foto";
   item.setText(type+" · "+DateFormat.getDateTimeInstance().format(new Date(f.lastModified()))+"\n"+f.getName());
   item.setOnClickListener(v->show(f));list.addView(item,new LinearLayout.LayoutParams(-1,-2));
  }
 }
 private void clearSelection(){
  selected=null;player.stopPlayback();player.setVisibility(android.view.View.GONE);image.setImageDrawable(null);image.setVisibility(android.view.View.GONE);
 }
 private void show(File f){
  clearSelection();selected=f;info.setText(f.getName()+" · "+f.length()/1024+" KB");
  if(f.getName().endsWith(".partial")){info.append("\nArchivo incompleto conservado. Su recuperación no está garantizada.");return;}
  if(f.getName().endsWith(".mp4")){
   player.setVisibility(android.view.View.VISIBLE);player.setVideoPath(f.getAbsolutePath());player.setOnPreparedListener(mp->player.start());return;
  }
  BitmapFactory.Options bounds=new BitmapFactory.Options();bounds.inJustDecodeBounds=true;BitmapFactory.decodeFile(f.getAbsolutePath(),bounds);
  BitmapFactory.Options opts=new BitmapFactory.Options();opts.inSampleSize=1;
  while(bounds.outWidth/opts.inSampleSize>1600||bounds.outHeight/opts.inSampleSize>1600)opts.inSampleSize*=2;
  android.graphics.Bitmap bitmap=BitmapFactory.decodeFile(f.getAbsolutePath(),opts);
  if(bitmap==null){info.setText("No se pudo abrir la foto.");return;}
  image.setImageBitmap(bitmap);image.setVisibility(android.view.View.VISIBLE);
 }
 private void confirmDelete(){
  final File f=selected;if(f==null){Toast.makeText(this,"Elegí un archivo",Toast.LENGTH_SHORT).show();return;}
  new AlertDialog.Builder(this).setTitle("Eliminar archivo").setMessage("¿Eliminar "+f.getName()+"? No se puede deshacer.")
   .setNegativeButton("Cancelar",null).setPositiveButton("Eliminar",(d,w)->{clearSelection();boolean removed=f.delete();refresh();if(!removed)info.setText("No se pudo eliminar el archivo.");}).show();
 }
 @Override protected void onPause(){player.pause();super.onPause();}
 @Override protected void onDestroy(){clearSelection();super.onDestroy();}
}
