package com.vigia.app;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Context;
import android.os.Build;
/** Local silent event alerts. Paired watch delivery is controlled by its companion app. */
public final class WatchAlerts {
 private static final String CHANNEL="vigia_events";
 private WatchAlerts(){}
 public static void recordingStarted(Context context) { send(context,"Grabación iniciada"); }
 public static void testAlert(Context context) { send(context,"Prueba de alerta al reloj"); }
 private static void send(Context context,String message) {
  NotificationManager manager=(NotificationManager)context.getSystemService(Context.NOTIFICATION_SERVICE);
  if(manager==null)return;
  if(Build.VERSION.SDK_INT>=26) {
   NotificationChannel channel=new NotificationChannel(CHANNEL,"Eventos VIGÍA",NotificationManager.IMPORTANCE_DEFAULT);
   channel.setSound(null,null);channel.enableVibration(false);
   manager.createNotificationChannel(channel);
  }
  Notification.Builder builder=Build.VERSION.SDK_INT>=26?new Notification.Builder(context,CHANNEL):new Notification.Builder(context);
  Notification n=builder.setSmallIcon(android.R.drawable.presence_video_online)
    .setContentTitle("VIGÍA").setContentText(message)
    .setAutoCancel(true).setOnlyAlertOnce(true).build();
  manager.notify(101,n);
 }
}
