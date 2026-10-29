from pathlib import Path
import os,re
root=Path(os.environ["PROJECT"])
files=[root/"app/build.gradle",root/"app/build.gradle.kts"]
p=next((x for x in files if x.exists()),None)
assert p,"Android module Gradle file not found"
s=p.read_text()
code=int(os.environ.get("GITHUB_RUN_NUMBER","1000"))+10000
# APK updater needs monotonically increasing versionCode across CI builds.
s,n=re.subn(r'(versionCode\s*(?:=\s*)?)\d+',lambda m:m.group(1)+str(code),s,count=1)
assert n==1,"versionCode not found"
s,n=re.subn(r'(versionName\s*(?:=\s*)?["\'])[^"\']+(["\'])',lambda m:m.group(1)+"8.4."+str(code)+m.group(2),s,count=1)
assert n==1,"versionName not found"
p.write_text(s)
print("APK versionCode",code,"in",p)
