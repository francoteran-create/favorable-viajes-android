from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
start=s.index(" int importClock(InputStream in)throws Exception{")
end=s.index("  NodeList rows=doc.getElementsByTagNameNS",start)
part=s[start:end]
old='''  f.setFeature("http://apache.org/xml/features/disallow-doctype-decl",true);
  f.setFeature("http://xml.org/sax/features/external-general-entities",false);
  f.setFeature("http://xml.org/sax/features/external-parameter-entities",false);
  f.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd",false);
  f.setXIncludeAware(false);f.setExpandEntityReferences(false);
  Document doc=f.newDocumentBuilder().parse(in);'''
new='''  // Android XML factories vary by device: only enable supported protection flags.
  try{f.setFeature("http://apache.org/xml/features/disallow-doctype-decl",true);}catch(Exception ignored){}
  try{f.setFeature("http://xml.org/sax/features/external-general-entities",false);}catch(Exception ignored){}
  try{f.setFeature("http://xml.org/sax/features/external-parameter-entities",false);}catch(Exception ignored){}
  try{f.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd",false);}catch(Exception ignored){}
  try{f.setFeature(javax.xml.XMLConstants.FEATURE_SECURE_PROCESSING,true);}catch(Exception ignored){}
  try{f.setXIncludeAware(false);}catch(Exception ignored){}
  f.setExpandEntityReferences(false);
  javax.xml.parsers.DocumentBuilder builder=f.newDocumentBuilder();
  builder.setEntityResolver((publicId,systemId)->new org.xml.sax.InputSource(new java.io.StringReader("")));
  Document doc=builder.parse(in);'''
assert old in part, "Old clock parser fragment missing"
s=s[:start]+part.replace(old,new)+s[end:]
# No misleading successful import when no rows match the configured date/time format.
needle='''   w.setTransactionSuccessful();
  }finally{w.endTransaction();}
  return add;
 }'''
# Do not treat zero new records as a failure: repeated file imports are intentionally idempotent.
assert needle in s[start:]
p.write_text(s)
print("V69 logs XLS: Android compatible secure XML handling, report importer preserved")
