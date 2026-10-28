"""Sign the obfuscated release APK only when the owner's GitHub signing secret exists.
The actual keystore must NEVER enter the repository or build artifact.
"""
import base64
import glob
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

bundle=os.getenv("NAUTILUS_RELEASE_SIGNING_BUNDLE", "").strip()
if not bundle:
    print("PILOT ONLY: NAUTILUS_RELEASE_SIGNING_BUNDLE is not configured.")
    sys.exit(0)
cfg=json.loads(base64.b64decode(bundle,validate=True))
assert cfg.get("version")==1 and cfg.get("alias")=="nautilus-release", "Invalid release signer profile"
data=base64.b64decode(cfg["keystore_b64"],validate=True)
assert len(data)>1500 and len(data)<100000, "Invalid keystore"
password=cfg["password"]
assert len(password)>=20 and "\n" not in password and "\r" not in password
project=Path(os.environ["PROJECT"])
apks=glob.glob(str(project/"app/build/outputs/apk/release/*-unsigned.apk"))
assert len(apks)==1, "Expected one unsigned obfuscated release APK"
buildtools=sorted(glob.glob(str(Path(os.environ["ANDROID_HOME"])/"build-tools/*/apksigner")))
assert buildtools, "Android apksigner is missing"
out=Path("out/Nautilus-Presentismo-MASTER-FIRMADA.apk")
out.parent.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory(prefix="nautilus-sign-") as temp:
    key=Path(temp)/"release.p12"
    key.write_bytes(data)
    key.chmod(0o600)
    env=os.environ.copy()
    env["NAUTILUS_MASTER_STORE_PASS"]=password
    # PKCS12 uses the same password for store and private key.
    cmd=[buildtools[-1],"sign","--ks",str(key),"--ks-type","PKCS12",
      "--ks-key-alias","nautilus-release","--ks-pass","env:NAUTILUS_MASTER_STORE_PASS",
      "--key-pass","env:NAUTILUS_MASTER_STORE_PASS",
      "--v1-signing-enabled","true","--v2-signing-enabled","true",
      "--out",str(out),apks[0]]
    subprocess.run(cmd,env=env,check=True)
    subprocess.run([buildtools[-1],"verify","--verbose","--print-certs",str(out)],check=True)
assert out.is_file() and out.stat().st_size>100000, "Signed APK missing"
print("PASS: release APK obfuscated, signed with the persistent owner key and verified.")
