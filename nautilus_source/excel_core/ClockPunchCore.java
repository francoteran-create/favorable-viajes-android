package ar.com.nautiluscountry.presentismo;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringReader;
import java.text.ParsePosition;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.LinkedHashMap;
import java.util.Locale;
import javax.xml.XMLConstants;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;

/** Parses Attendance logs.xls in XML Spreadsheet 2003 format, not binary BIFF or XLSX. */
public final class ClockPunchCore {
  public static final int MAX_INPUT_BYTES=24*1024*1024;
  public static final int MAX_ROWS=180000;
  public static final class Punch {
    public final String id,name,stamp,device;
    Punch(String id,String name,String stamp,String device){
      this.id=id;this.name=name;this.stamp=stamp;this.device=device;
    }
  }
  private ClockPunchCore(){}
  private static void feature(DocumentBuilderFactory factory,String name,boolean on){
    try{factory.setFeature(name,on);}catch(Exception ignored){}
  }
  private static String canonicalDate(String raw){
    if(raw==null)return null;
    String t=raw.trim();
    String[] formats={"yyyy-MM-dd'T'HH:mm:ss","yyyy-MM-dd HH:mm:ss",
      "yyyy/MM/dd HH:mm:ss","dd/MM/yyyy HH:mm:ss",
      "yyyy-MM-dd'T'HH:mm","yyyy-MM-dd HH:mm",
      "yyyy/MM/dd HH:mm","dd/MM/yyyy HH:mm"};
    for(String format:formats){
      SimpleDateFormat parser=new SimpleDateFormat(format,Locale.US);
      parser.setLenient(false);
      ParsePosition pos=new ParsePosition(0);
      Date date=parser.parse(t,pos);
      if(date!=null&&pos.getIndex()==t.length()){
        SimpleDateFormat result=new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss",Locale.US);
        return result.format(date);
      }
    }
    return null;
  }
  private static ArrayList<String> cells(Element row){
    // SpreadsheetML ss:Index allows sparse columns.
    ArrayList<String> out=new ArrayList<>();
    NodeList nodes=row.getElementsByTagNameNS("*","Cell");
    int position=0;
    for(int i=0;i<nodes.getLength();i++){
      Element cell=(Element)nodes.item(i);
      String index=cell.getAttributeNS("urn:schemas-microsoft-com:office:spreadsheet","Index");
      if(!index.isEmpty()){
        try{position=Integer.parseInt(index)-1;}catch(Exception bad){return new ArrayList<>();}
      }
      if(position<0||position>150)return new ArrayList<>();
      while(out.size()<=position)out.add("");
      NodeList data=cell.getElementsByTagNameNS("*","Data");
      out.set(position,data.getLength()==0?"":data.item(0).getTextContent().trim());
      position++;
    }
    return out;
  }
  private static String at(ArrayList<String> cells,int i){
    return i<0||i>=cells.size()?"":cells.get(i).trim();
  }
  public static ArrayList<Punch> parse(InputStream input)throws Exception{
    if(input==null)throw new IOException("No se seleccionó el archivo de fichadas");
    ByteArrayOutputStream out=new ByteArrayOutputStream();
    byte[] chunk=new byte[8192];int n,total=0;
    while((n=input.read(chunk))!=-1){
      total+=n;if(total>MAX_INPUT_BYTES)throw new IOException("Archivo de fichadas demasiado grande (máximo 24 MB)");
      out.write(chunk,0,n);
    }
    byte[] bytes=out.toByteArray();
    int k=0;
    if(bytes.length>=3&&(bytes[0]&255)==239&&(bytes[1]&255)==187&&(bytes[2]&255)==191)k=3;
    while(k<bytes.length&&(bytes[k]==' '||bytes[k]=='\r'||bytes[k]=='\n'||bytes[k]=='\t'))k++;
    if(k>=bytes.length||bytes[k]!='<')throw new IOException(
      "Formato no reconocido: exportá Attendance logs como Excel XML (no XLS binario ni XLSX)");
    DocumentBuilderFactory factory=DocumentBuilderFactory.newInstance();
    factory.setNamespaceAware(true);
    feature(factory,"http://apache.org/xml/features/disallow-doctype-decl",true);
    feature(factory,"http://xml.org/sax/features/external-general-entities",false);
    feature(factory,"http://xml.org/sax/features/external-parameter-entities",false);
    feature(factory,"http://apache.org/xml/features/nonvalidating/load-external-dtd",false);
    feature(factory,XMLConstants.FEATURE_SECURE_PROCESSING,true);
    try{factory.setXIncludeAware(false);}catch(Exception ignored){}
    factory.setExpandEntityReferences(false);
    DocumentBuilder builder=factory.newDocumentBuilder();
    builder.setEntityResolver((publicId,systemId)->new InputSource(new StringReader("")));
    Document document=builder.parse(new ByteArrayInputStream(bytes));
    if(document.getDoctype()!=null||document.getDocumentElement()==null||
      !"Workbook".equals(document.getDocumentElement().getLocalName()))
      throw new IOException("No es un archivo Excel XML de fichadas válido");
    NodeList rows=document.getElementsByTagNameNS("*","Row");
    if(rows.getLength()>MAX_ROWS)throw new IOException("El reporte tiene demasiadas filas");
    int header=-1,idCol=-1,nameCol=-1,timeCol=-1,deviceCol=-1;
    for(int i=0;i<Math.min(rows.getLength(),40);i++){
      ArrayList<String> cells=cells((Element)rows.item(i));
      int id=-1,name=-1,time=-1,device=-1;
      for(int j=0;j<cells.size();j++){
        String col=cells.get(j).toLowerCase(Locale.ROOT).trim();
        if(col.equals("id.")||col.equals("id"))id=j;
        else if(col.equals("name")||col.equals("nombre"))name=j;
        else if(col.equals("att.time")||col.equals("att time")||col.equals("fecha/hora")||
          col.equals("fecha y hora"))time=j;
        else if(col.equals("device id")||col.equals("dispositivo"))device=j;
      }
      if(id>=0&&name>=0&&time>=0){
        header=i;idCol=id;nameCol=name;timeCol=time;deviceCol=device;break;
      }
    }
    if(header<0)throw new IOException("Faltan columnas ID., Name y Att.Time en Attendance logs");
    // Preserve the original row order; let SQLite reject duplicates using its existing unique constraints.
    ArrayList<Punch> result=new ArrayList<>();
    for(int i=header+1;i<rows.getLength();i++){
      ArrayList<String> row=cells((Element)rows.item(i));
      String id=at(row,idCol),name=at(row,nameCol),device=at(row,deviceCol);
      String stamp=canonicalDate(at(row,timeCol));
      if(id.matches("[0-9]{1,16}")&&stamp!=null){
        if(name.length()>160)name=name.substring(0,160);
        if(device.length()>80)device=device.substring(0,80);
        result.add(new Punch(id,name,stamp,device));
      }
    }
    if(result.isEmpty())throw new IOException(
      "No hay fichadas con fecha válida. Verificá la columna Att.Time y el formato del reloj");
    return result;
  }
}
