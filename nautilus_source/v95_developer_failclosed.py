from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# The owner code generator is never exposed unless the matching signing key is present.
s=s.replace('if(!securityOwner||!securityUnlocked||!licDeveloperAuthorized()){secGate();return;}','if(!securityOwner||!securityUnlocked||!licDeveloperAuthorized()){securityUnlocked=false;securityOwner=false;securityPromptOpen=false;secGate();return;}')
# Prevent an invalid developer key or a failure to open file from leaving a privileged session.
old='if(result!=RESULT_OK||data==null){secAdminPanel();return;}'
assert old in s
s=s.replace(old,'''if(result!=RESULT_OK||data==null){
   securityUnlocked=false;securityOwner=false;securityPromptOpen=false;secGate();return;
  }''',1)
old='''.setPositiveButton("VOLVER",(x,y)->secAdminPanel()).show();
  }
 }
 void licCreate()'''
assert old in s
s=s.replace(old,'''.setPositiveButton("VOLVER",(x,y)->{
      securityUnlocked=false;securityOwner=false;securityPromptOpen=false;secGate();
    }).show();
  }
 }
 void licCreate()''',1)
# Match the title shown to ordinary administrators with the renamed owner role.
s=s.replace('Solicitá una nueva licencia al desarrollador.','Solicitá una nueva licencia al DESARROLLADOR.')
p.write_text(s)
print("V95 cleans developer session after failed authorization and blocks unauthorized owner menu")
