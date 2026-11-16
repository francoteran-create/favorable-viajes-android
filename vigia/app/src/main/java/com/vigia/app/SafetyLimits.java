package com.vigia.app;
import android.content.Context;
import android.os.BatteryManager;
import android.os.StatFs;
/** Threshold policy for future recorder integration. No camera or file I/O here. */
public final class SafetyLimits {
 public enum Mode { NORMAL, SEGMENT_30_SECONDS, STOP_AND_FINALIZE }
 private SafetyLimits(){}
 public static Mode evaluate(int batteryPercent,long freeBytes) {
  long mb=1024L*1024L;
  if(batteryPercent<=5 || freeBytes<100L*mb) return Mode.STOP_AND_FINALIZE;
  if(batteryPercent<=15 || freeBytes<250L*mb) return Mode.SEGMENT_30_SECONDS;
  return Mode.NORMAL;
 }
 public static int batteryPercent(Context context) {
  BatteryManager manager=(BatteryManager)context.getSystemService(Context.BATTERY_SERVICE);
  return manager==null?-1:manager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY);
 }
 public static long availableBytes(Context context) {
  java.io.File volume=context.getExternalFilesDir(null);
  if(volume==null) return 0L;
  StatFs stat=new StatFs(volume.getAbsolutePath());
  return stat.getAvailableBytes();
 }
 public static Mode currentMode(Context context) {
  int battery=batteryPercent(context);
  if(battery<0 || battery>100) return Mode.STOP_AND_FINALIZE; // fail safe
  try { return evaluate(battery,availableBytes(context)); }
  catch(RuntimeException e){return Mode.STOP_AND_FINALIZE;}
 }
}
