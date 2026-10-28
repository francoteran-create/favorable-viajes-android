from pathlib import Path
import os,re
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
public="MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtTyZX9nDcLVw2rYz7Z3REPyrPVeJOwp7SlSXYLjzudzj+BbxtOa45gajGsdDYYaOPDHjSMZBmV/njfjcuRZOvFifbU+Nyu5ARFwJ3ufW3Q9YyDgesXdlC2hd/9xLHrU2A7ym9e6y/2xe09HuKis9JZxIpOgKo6UgXkgVQ0jH2vXrRIahEke+Aw17BfztqEhqxIWXsFhDMiZ9irHlI/KPKUvhxJfdcCWn2NjVZbrLw0kzjLm6Taujw0XzyagtXteDTLGSNxwCyDlEmEfbfEpRwKNrB4d1Roe52ePQul3caOKt7sKInT4CCm3swhUfSHr2+SyNRNpzusLS3dcVv7JU/wIDAQAB"
s,count=re.subn(r'static final String LICENSE_PUBLIC_KEY="[^"]+";','static final String LICENSE_PUBLIC_KEY="'+public+'";',s,count=1)
assert count==1
p.write_text(s)
print("V104 RSA public key paired with privately delivered developer key")
