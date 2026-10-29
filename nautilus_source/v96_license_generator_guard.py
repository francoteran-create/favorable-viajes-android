from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
needle='''  if(!securityOwner||!securityUnlocked||!licDeveloperAuthorized()){securityUnlocked=false;securityOwner=false;securityPromptOpen=false;secGate();return;}'''
assert needle in s
# Ensure operator functions and the developer controls are only accessible with actual private-key possession.
old='''void licCreate(){
  if(!securityOwner||!securityUnlocked||!licDeveloperAuthorized())return;'''
assert old in s
s=s.replace(old,'''void licCreate(){
  if(!securityOwner||!securityUnlocked||!licDeveloperAuthorized()){
   securityUnlocked=false;securityOwner=false;securityPromptOpen=false;secGate();return;
  }''',1)
# Set the developer label consistently on the expired licensing screen.
s=s.replace('Solicitá una nueva licencia al desarrollador.','Solicitá una nueva licencia al DESARROLLADOR.')
p.write_text(s)
print("V96 developer code emission guarded by live cryptographic possession")
