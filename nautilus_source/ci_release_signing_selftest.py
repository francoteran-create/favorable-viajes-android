"""CI test: sign the actual minified release with an ephemeral key, never publish this APK."""
import base64
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile

password=secrets.token_urlsafe(32)
with tempfile.TemporaryDirectory(prefix="nautilus-throwaway-key-") as d:
    store=Path(d)/"smoke.p12"
    subprocess.run(["keytool","-genkeypair","-keystore",str(store),"-storetype","PKCS12",
      "-alias","nautilus-release","-keyalg","RSA","-keysize","2048",
      "-validity","1","-storepass",password,"-keypass",password,
      "-dname","CN=CI TEMPORARY TEST SIGNER, O=NAUTILUS"],check=True,
      stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    bundle={"version":1,"alias":"nautilus-release","password":password,
      "keystore_b64":base64.b64encode(store.read_bytes()).decode("ascii")}
    env=os.environ.copy()
    env["NAUTILUS_RELEASE_SIGNING_BUNDLE"]=base64.b64encode(
      json.dumps(bundle,separators=(",",":")).encode("utf-8")).decode("ascii")
    output=Path(os.environ["RUNNER_TEMP"])/"nautilus-smoke-signed-release.apk"
    env["NAUTILUS_SIGNED_OUTPUT"]=str(output)
    subprocess.run([sys.executable,"nautilus_source/ci_sign_release.py"],check=True,env=env)
    assert output.is_file() and output.stat().st_size>100000
print("PASS: real obfuscated release was signed and verified with throwaway CI certificate; NOT distributable.")
