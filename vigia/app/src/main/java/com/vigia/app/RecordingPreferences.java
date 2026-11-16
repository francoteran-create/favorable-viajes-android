package com.vigia.app;
import android.content.Context;
import android.content.SharedPreferences;
/** Persisted user choices; camera integration is still pending. */
public final class RecordingPreferences {
 private static final String NAME="vigia_settings";
 private RecordingPreferences(){}
 public static void save(Context c,int resolution,int seconds,boolean photos,boolean audio){
  if(resolution!=480&&resolution!=720&&resolution!=1080)throw new IllegalArgumentException("resolution");
  if(seconds!=10&&seconds!=30&&seconds!=60)throw new IllegalArgumentException("duration");
  c.getSharedPreferences(NAME,Context.MODE_PRIVATE).edit()
   .putInt("resolution",resolution).putInt("seconds",seconds)
   .putBoolean("photos",photos).putBoolean("audio",audio).apply();
 }
 public static SharedPreferences get(Context c){return c.getSharedPreferences(NAME,Context.MODE_PRIVATE);}
}
