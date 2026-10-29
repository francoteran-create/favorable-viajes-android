from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
old='long now=System.currentTimeMillis(),last=licPrefs().getLong("last_seen",0);'
assert old in s
new='''long now=System.currentTimeMillis(),last=licPrefs().getLong("last_seen",0);
  long elapsed=android.os.SystemClock.elapsedRealtime();
  long priorElapsed=licPrefs().getLong("prior_elapsed",0);
  long priorWall=licPrefs().getLong("prior_wall",0);
  if(priorElapsed>0&&elapsed>=priorElapsed&&priorWall>0){
    if(now+600000L<priorWall+(elapsed-priorElapsed))return false;
  }
  licPrefs().edit().putLong("prior_elapsed",elapsed).putLong("prior_wall",now).apply();'''
s=s.replace(old,new,1)
p.write_text(s)
print("V92 offline clock rollback check applied")
