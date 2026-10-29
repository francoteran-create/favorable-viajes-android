from pathlib import Path
import os,re
root=Path(os.environ["PROJECT"])
manifest=root/"app/src/main/AndroidManifest.xml"
s=manifest.read_text(encoding="utf-8")
assert "<application" in s and "</application>" in s
start=s.index("<application")
end=s.index(">",start)
head=s[start:end]
for attr,value in {
 "android:allowBackup":"false",
 "android:fullBackupContent":"false",
 "android:usesCleartextTraffic":"false"
}.items():
 if re.search(r'\\b'+re.escape(attr)+r'="[^"]*"',head):
  head=re.sub(r'\\b'+re.escape(attr)+r'="[^"]*"',attr+'="'+value+'"',head)
 else:
  head+=' '+attr+'="'+value+'"'
s=s[:start]+head+s[end:]
manifest.write_text(s,encoding="utf-8")
print("Nautilus release hardening: backup and cleartext traffic restricted in manifest")
