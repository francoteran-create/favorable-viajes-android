from pathlib import Path
import base64, math, os, re, struct, wave

root=Path(os.environ["PROJECT"])
main=root/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
manifest=root/"app/src/main/AndroidManifest.xml"
asset=Path(__file__).with_name("v119_launcher_icon.b64")
icon=base64.b64decode("".join(asset.read_text().split()),validate=True)
assert len(icon)>3000 and icon[:4]==b"RIFF" and icon[8:12]==b"WEBP"
draw=root/"app/src/main/res/drawable-nodpi"
draw.mkdir(parents=True,exist_ok=True)
(draw/"nautilus_launcher.webp").write_bytes(icon)

# Android must use the approved boat as the actual launcher icon, not just a bitmap in the UI.
xml=manifest.read_text(encoding="utf-8")
m=re.search(r"<application\b[^>]*>",xml,re.S)
assert m, "No application tag in manifest"
tag=m.group()
tag=re.sub(r'\s+android:(?:roundIcon|icon)="[^"]*"', "", tag)
tag=tag[:-1]+' android:icon="@drawable/nautilus_launcher" android:roundIcon="@drawable/nautilus_launcher">'
xml=xml[:m.start()]+tag+xml[m.end():]
manifest.write_text(xml,encoding="utf-8")

# Pre-render the original deep mysterious electronic cue as a real WAV Android resource.
# A file-backed MediaPlayer is more reliable than the previous threaded raw AudioTrack.
raw=root/"app/src/main/res/raw"
raw.mkdir(parents=True,exist_ok=True)
rate=22050
duration=0.94
frames=bytearray()
phase=0.0
for n in range(round(rate*duration)):
 t=n/rate
 if t<0.32: f=112+38*t/0.32
 elif t<0.59: f=150-32*(t-0.32)/0.27
 else: f=118-27*(t-0.59)/0.35
 f+=2.6*math.sin(2*math.pi*6.3*t)
 phase+=2*math.pi*f/rate
 attack=min(1.,t/0.065)
 release=min(1.,(duration-t)/0.22)
 envelope=max(0.,attack)*max(0.,release)
 pulse=0.84+0.16*math.cos(2*math.pi*3.7*t)
 tone=0.78*math.sin(phase)+0.16*math.sin(2.012*phase)+0.06*math.sin(3.97*phase)
 low=0.08*math.sin(phase*0.48)
 amp=int((tone+low)*envelope*pulse*7600)
 amp=max(-32767,min(32767,amp))
 frames+=struct.pack("<h",amp)
with wave.open(str(raw/"nautilus_start.wav"),"wb") as w:
 w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(bytes(frames))

s=main.read_text(encoding="utf-8")
start=s.index(" // V118: original, short, low-pitched robotic startup chirp.")
end=s.index(" void secSplash(){",start)
method=String = r'''
 // V119: quiet, low, mysterious original robot tone. Embedded WAV / MediaPlayer.
 void ntPlayLaunchSound(){
  try{
   android.media.AudioManager mgr=(android.media.AudioManager)getSystemService(AUDIO_SERVICE);
   if(mgr==null || mgr.getRingerMode()!=android.media.AudioManager.RINGER_MODE_NORMAL)return;
   if(mgr.getStreamVolume(android.media.AudioManager.STREAM_MUSIC)==0)return;
   final android.media.MediaPlayer sound=android.media.MediaPlayer.create(this,R.raw.nautilus_start);
   if(sound==null)return;
   sound.setVolume(0.24f,0.24f);
   sound.setOnCompletionListener(mp->{try{mp.release();}catch(Exception ignored){}});
   sound.setOnErrorListener((mp,what,extra)->{try{mp.release();}catch(Exception ignored){}return true;});
   sound.start();
  }catch(Exception ignored){}
 }
'''
s=s[:start]+method+"\n"+s[end:]
main.write_text(s,encoding="utf-8")
print("V119 launcher: approved gold sailboat as Android launcher; quiet original WAV sound on startup")
