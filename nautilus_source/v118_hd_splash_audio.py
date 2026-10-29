from pathlib import Path
import os

root = Path(os.environ["PROJECT"])
java = root / "app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
source = root / "app/src/main/res/drawable/proyecto_cero_splash.jpg"
target_dir = root / "app/src/main/res/drawable-nodpi"
target_dir.mkdir(parents=True, exist_ok=True)
assert source.exists() and source.stat().st_size > 250000, "Original full-resolution splash is missing"
target = target_dir / "proyecto_cero_splash.jpg"
source.replace(target)
s = java.read_text(encoding="utf-8")
old = 'art.setScaleType(android.widget.ImageView.ScaleType.CENTER_CROP);'
assert s.count(old) == 1, "Splash scaling hook moved"
s = s.replace(old, 'art.setScaleType(android.widget.ImageView.ScaleType.FIT_CENTER);\n  art.setBackgroundColor(android.graphics.Color.BLACK);', 1)
old = 'splash.setContentView(art);splash.setCancelable(false);splash.show();'
assert s.count(old) == 1, "Splash display hook moved"
s = s.replace(old, old + '\n  ntPlayLaunchSound();', 1)
old = '},1000);\n }\n void secLogin(){'
assert s.count(old) == 1, "Splash duration hook moved"
s = s.replace(old, '},1350);\n }\n void secLogin(){', 1)

sound = r'''
 // V118: original, short, low-pitched robotic startup chirp.
 // Synthesized locally: no Star Wars audio samples or external media.
 void ntPlayLaunchSound(){
  new Thread(()->{
   android.media.AudioTrack track=null;
   try{
    android.media.AudioManager mgr=(android.media.AudioManager)getSystemService(AUDIO_SERVICE);
    if(mgr!=null && mgr.getRingerMode()!=android.media.AudioManager.RINGER_MODE_NORMAL)return;
    final int rate=22050;
    final int length=(int)(rate*1.05);
    byte[] pcm=new byte[length*2];
    double phase=0.0;
    for(int i=0;i<length;i++){
     double t=i/(double)rate;
     double frequency;
     if(t<0.27)frequency=122.0+175.0*t/0.27;
     else if(t<0.53)frequency=297.0-142.0*(t-0.27)/0.26;
     else if(t<0.81)frequency=163.0+68.0*Math.sin(2.0*Math.PI*7.0*(t-0.53));
     else frequency=142.0-48.0*(t-0.81)/0.24;
     phase+=2.0*Math.PI*frequency/rate;
     double onset=Math.min(1.0,t*36.0);
     double decay=Math.min(1.0,(1.05-t)*13.0);
     double gate=(t>0.335&&t<0.392)||(t>0.712&&t<0.760)?0.06:1.0;
     double modulation=0.79+0.21*Math.sin(2.0*Math.PI*17.0*t);
     double tone=0.65*Math.sin(phase)+0.25*Math.sin(2.01*phase)+0.10*Math.sin(phase*0.50);
     int amp=(int)(tone*onset*decay*gate*modulation*11000.0);
     amp=Math.max(-32767,Math.min(32767,amp));
     pcm[i*2]=(byte)(amp&255);
     pcm[i*2+1]=(byte)((amp>>8)&255);
    }
    track=new android.media.AudioTrack(
     android.media.AudioManager.STREAM_MUSIC,rate,
     android.media.AudioFormat.CHANNEL_OUT_MONO,
     android.media.AudioFormat.ENCODING_PCM_16BIT,
     pcm.length,android.media.AudioTrack.MODE_STATIC);
    if(track.getState()!=android.media.AudioTrack.STATE_INITIALIZED)return;
    if(track.write(pcm,0,pcm.length)!=pcm.length)return;
    track.setVolume(0.45f);
    track.play();
    Thread.sleep(1150L);
   }catch(Exception ignored){}
   finally{if(track!=null){try{track.stop();}catch(Exception ignored){}try{track.release();}catch(Exception ignored){}}}
  },"NautilusLaunchSound").start();
 }
'''
marker=' void secSplash(){'
assert s.count(marker)==1,"Splash entry hook moved"
s=s.replace(marker,sound+'\n'+marker,1)
java.write_text(s,encoding="utf-8")
print("V118: full-HD 941x1672 splash preserved in drawable-nodpi; original low robotic startup audio installed")
