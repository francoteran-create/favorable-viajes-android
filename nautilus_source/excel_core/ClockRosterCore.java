package ar.com.nautiluscountry.presentismo;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import javax.xml.XMLConstants;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;

/** Parses biometric Attendance Report exports in XML Spreadsheet 2003 (.xls) format.
 * A binary BIFF .xls or modern zipped .xlsx is NOT this format.
 */
public final class ClockRosterCore {
  public static final int MAX_INPUT_BYTES = 12 * 1024 * 1024;
  public static final int MAX_ROWS = 150000;
  private static final Pattern HEADER = Pattern.compile(
      "ID\\.:\\s*(\\d{1,16})\\s+Name:\\s*(.*?)\\s+Dept\\.Name:\\s*(.*)",
      Pattern.CASE_INSENSITIVE | Pattern.DOTALL);
  private ClockRosterCore() {}

  private static void setting(DocumentBuilderFactory factory, String name, boolean enabled) {
    try { factory.setFeature(name, enabled); } catch(Exception unsupported) { /* Android variants */ }
  }

  public static LinkedHashMap<String,String[]> parse(InputStream input) throws Exception {
    if(input==null) throw new IOException("No se seleccionó un archivo");
    // No unbounded InputStream consumed by DOM; fail before a large input exhausts RAM.
    ByteArrayOutputStream buffer = new ByteArrayOutputStream();
    byte[] block=new byte[8192];
    int n, total=0;
    while((n=input.read(block))!=-1) {
      total+=n;
      if(total>MAX_INPUT_BYTES) throw new IOException("Reporte demasiado grande (máximo 12 MB)");
      buffer.write(block,0,n);
    }
    byte[] bytes=buffer.toByteArray();
    if(bytes.length==0) throw new IOException("El reporte está vacío");
    // Reject binary Excel early with a useful message instead of misleading XML failures.
    int k=0;
    if(bytes.length>=3 && (bytes[0]&255)==239 && (bytes[1]&255)==187 && (bytes[2]&255)==191)k=3;
    while(k<bytes.length && (bytes[k]==' '||bytes[k]=='\n'||bytes[k]=='\r'||bytes[k]=='\t'))k++;
    // XML declaration begins <?xml; some valid SpreadsheetML starts <Workbook.
    if(k>=bytes.length || bytes[k]!='<') throw new IOException(
      "Formato no reconocido: se requiere reporte Excel XML (Spreadsheet 2003), no XLS binario ni XLSX");

    DocumentBuilderFactory factory=DocumentBuilderFactory.newInstance();
    factory.setNamespaceAware(true);
    setting(factory, "http://apache.org/xml/features/disallow-doctype-decl", true);
    setting(factory, "http://xml.org/sax/features/external-general-entities", false);
    setting(factory, "http://xml.org/sax/features/external-parameter-entities", false);
    setting(factory, "http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
    setting(factory, XMLConstants.FEATURE_SECURE_PROCESSING, true);
    try {factory.setXIncludeAware(false);}catch(Exception ignored){}
    factory.setExpandEntityReferences(false);
    DocumentBuilder builder=factory.newDocumentBuilder();
    builder.setEntityResolver((publicId,systemId)->new InputSource(new StringReader("")));
    Document doc=builder.parse(new java.io.ByteArrayInputStream(bytes));
    if(doc.getDoctype()!=null) throw new IOException("DOCTYPE no permitido en reportes Excel");
    if(doc.getDocumentElement()==null ||
       !"Workbook".equals(doc.getDocumentElement().getLocalName())) {
      throw new IOException("Se esperaba Workbook de Excel XML");
    }
    NodeList rows=doc.getElementsByTagNameNS("*","Row");
    if(rows.getLength()>MAX_ROWS) throw new IOException("Demasiadas filas en reporte");
    LinkedHashMap<String,String[]> found=new LinkedHashMap<>();
    for(int i=0;i<rows.getLength();i++) {
      Element row=(Element)rows.item(i);
      NodeList cells=row.getElementsByTagNameNS("*","Data");
      for(int j=0;j<cells.getLength();j++) {
        String raw=cells.item(j).getTextContent();
        if(raw==null||raw.length()>1024)continue;
        Matcher m=HEADER.matcher(raw);
        if(m.find()){
          String id=m.group(1).trim();
          String name=m.group(2).trim();
          String sector=m.group(3).trim();
          if(!name.isEmpty() && name.length()<=160 && sector.length()<=160)
            found.put(id,new String[]{name,sector});
          break;
        }
      }
    }
    if(found.isEmpty()) throw new IOException(
      "No se encontraron empleados con ID., Name y Dept.Name en Attendance Report");
    return found;
  }
}
