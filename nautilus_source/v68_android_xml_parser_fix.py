from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
old='''  factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl",true);
  factory.setFeature("http://xml.org/sax/features/external-general-entities",false);
  factory.setFeature("http://xml.org/sax/features/external-parameter-entities",false);
  factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd",false);
  factory.setXIncludeAware(false);factory.setExpandEntityReferences(false);
  org.w3c.dom.Document doc=factory.newDocumentBuilder().parse(in);'''
new='''  // Android's platform XML parser does not support every Apache Xerces feature.
  // Unsupported security options must not abort legitimate SpreadsheetML imports.
  try{factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl",true);}catch(Exception ignored){}
  try{factory.setFeature("http://xml.org/sax/features/external-general-entities",false);}catch(Exception ignored){}
  try{factory.setFeature("http://xml.org/sax/features/external-parameter-entities",false);}catch(Exception ignored){}
  try{factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd",false);}catch(Exception ignored){}
  try{factory.setFeature(javax.xml.XMLConstants.FEATURE_SECURE_PROCESSING,true);}catch(Exception ignored){}
  try{factory.setXIncludeAware(false);}catch(Exception ignored){}
  factory.setExpandEntityReferences(false);
  javax.xml.parsers.DocumentBuilder builder=factory.newDocumentBuilder();
  builder.setEntityResolver((publicId,systemId)->new org.xml.sax.InputSource(new java.io.StringReader("")));
  org.w3c.dom.Document doc=builder.parse(in);'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)
print("V68 Android-compatible protected SpreadsheetML parsing")
