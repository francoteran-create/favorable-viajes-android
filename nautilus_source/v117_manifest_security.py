from pathlib import Path
import os
import re

root = Path(os.environ["PROJECT"])
manifest = root / "app/src/main/AndroidManifest.xml"
content = manifest.read_text(encoding="utf-8")
assert "<application" in content and "</application>" in content

start = content.index("<application")
end = content.index(">", start)
tag = content[start:end]
# Normalize all copies of each security setting; never append a duplicate.
for attr in ("allowBackup", "fullBackupContent", "usesCleartextTraffic"):
    tag = re.sub(r'\\s+android:' + attr + r'="[^"]*"', "", tag)
    # Replace handles old scripts that may have duplicated an attribute.
    tag = re.sub(r'\s+android:' + attr + r'="[^"]*"', "", tag)
    tag += f' android:{attr}="false"'
content = content[:start] + tag + content[end:]
manifest.write_text(content, encoding="utf-8")
for attr in ("allowBackup", "fullBackupContent", "usesCleartextTraffic"):
    assert tag.count("android:" + attr + "=") == 1, "Duplicate security attribute: " + attr
print("V117: manifest security attributes normalized without duplicates")
