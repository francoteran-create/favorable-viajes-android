#!/usr/bin/env python3
"""Fail CI if reconstructed Nautilus AndroidManifest weakens local-data privacy."""
import os
from pathlib import Path
import xml.etree.ElementTree as ET

project=Path(os.environ["PROJECT"])
manifest=project/"app/src/main/AndroidManifest.xml"
root=ET.parse(manifest).getroot()
app=root.find("application")
assert app is not None, "Missing application"
a="{http://schemas.android.com/apk/res/android}"
assert app.get(a+"allowBackup")=="false", "Android backup must be disabled"
assert app.get(a+"usesCleartextTraffic")=="false", "Cleartext traffic must be disabled"
assert app.get(a+"fullBackupContent")=="false", "Full backup must be disabled"
print("PASS: reconstructed Android manifest XML valid; backup and cleartext disabled")
