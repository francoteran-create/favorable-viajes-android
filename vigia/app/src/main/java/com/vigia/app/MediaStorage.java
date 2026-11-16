package com.vigia.app;
import android.content.Context;
import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
/** App-private media folders; not visible to Gallery or regular file managers. */
public final class MediaStorage {
 private MediaStorage(){}
 public static File videos(Context c){return ensure(new File(c.getExternalFilesDir(null),"Videos"));}
 public static File photos(Context c){return ensure(new File(c.getExternalFilesDir(null),"Fotos"));}
 private static File ensure(File dir){
  if(!dir.exists()&&!dir.mkdirs())throw new IllegalStateException("Cannot create "+dir);
  File nomedia=new File(dir,".nomedia");
  if(!nomedia.exists())try{nomedia.createNewFile();}catch(IOException e){throw new IllegalStateException(e);}
  return dir;
 }
 public static File nextVideo(Context c){return new File(videos(c),filename("VID_",".mp4"));}
 public static File nextPhoto(Context c){return new File(photos(c),filename("IMG_",".jpg"));}
 private static String filename(String prefix,String extension){
  return prefix+new SimpleDateFormat("yyyyMMdd_HHmmss_SSS",Locale.US).format(new Date())+extension;
 }
}
