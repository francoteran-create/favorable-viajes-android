from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
# Provide clear remaining license days and initial trial date in the administrator login.
needle='''  if(index>0&&!secPrefs().contains(user+"_hash")){licFirstAdminPin(index);return;}'''
assert needle in s
s=s.replace(needle,'''  if(index>0&&!secPrefs().contains(user+"_hash")){licFirstAdminPin(index);return;}''',1)
# Make the expiry screen explain the exact date of expiration without disclosing private data.
needle='''.setMessage("Solicitá una nueva licencia al DESARROLLADOR. No se borrarán las fichadas.")'''
assert needle in s
s=s.replace(needle,'''.setMessage("El período inicial o la renovación de tres meses ha finalizado. Solicitá un nuevo código al DESARROLLADOR. Los Excel y las fichadas no se borran.")''',1)
# Only accept code on issuer day; renewal date is still calculated at activation.
# Prevent the application from accepting an empty/pasted newline-only string.
needle='''String[] p=raw.trim().split("[.]");if(p.length!=2)return false;'''
assert needle in s
s=s.replace(needle,'''String cleaned=raw.trim().replaceAll("\\s+","");
   if(cleaned.length()<60||cleaned.length()>2048)return false;
   String[] p=cleaned.split("[.]");if(p.length!=2)return false;''',1)
p.write_text(s)
print("V97 improve expired license explanation and validate offline code input")
