package ar.com.nautiluscountry.presentismo;

import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;

public class ClockRosterCoreTest {
  private static int cases;
  private static void check(boolean ok,String detail) {
    cases++;if(!ok)throw new AssertionError(detail);
  }
  private static LinkedHashMap<String,String[]> parse(String xml) throws Exception {
    return ClockRosterCore.parse(new ByteArrayInputStream(xml.getBytes(StandardCharsets.UTF_8)));
  }
  private static void rejects(byte[] input,String detail) throws Exception {
    boolean blocked=false;
    try {ClockRosterCore.parse(new ByteArrayInputStream(input));}
    catch(Exception expected){blocked=true;}
    check(blocked,detail);
  }
  private static String row(String text) {
    return "<Row><Cell><Data ss:Type=\"String\">"+text+"</Data></Cell></Row>";
  }
  public static void main(String[] args) throws Exception {
    String head="<?xml version=\"1.0\"?><Workbook xmlns=\"urn:schemas-microsoft-com:office:spreadsheet\" "+
      "xmlns:ss=\"urn:schemas-microsoft-com:office:spreadsheet\"><Worksheet ss:Name=\"Personal\"><Table>";
    String tail="</Table></Worksheet></Workbook>";
    LinkedHashMap<String,String[]> records=parse(head+
      row("ID.: 0007 Name: Ana Pérez Dept.Name: Seguridad")+
      row("ID.: 42 Name: Pedro López Dept.Name: Mantenimiento")+tail);
    check(records.size()==2,"two employees");
    check("Ana Pérez".equals(records.get("0007")[0]),"Unicode and leading zeros");
    check("Seguridad".equals(records.get("0007")[1]),"sector parsed");
    check("Pedro López".equals(records.get("42")[0]),"second employee parsed");
    check(parse(head+row("ID.: 7 Name: Old Dept.Name: Limpieza")+
      row("ID.: 7 Name: New Dept.Name: Jardinería")+tail).get("7")[0].equals("New"),
      "duplicate employee latest row wins");
    check(parse(head+row("Not a personnel row")+
      row("ID.: 11 Name: Julia Dept.Name: Administración")+tail).size()==1,"ignore headings");
    check(parse("  "+head.replace("<?xml version=\"1.0\"?>","")+row("ID.: 21 Name: Juan Dept.Name: Seguridad")+tail).size()==1,
      "leading whitespace");
    check(parse("\uFEFF"+head+row("ID.: 21 Name: Juan Dept.Name: Seguridad")+tail).size()==1,
      "UTF8 BOM");
    rejects(new byte[]{(byte)0xd0,(byte)0xcf,0x11,(byte)0xe0},"reject binary .xls");
    rejects(new byte[]{'P','K',3,4},"reject .xlsx ZIP");
    rejects((head+tail).getBytes(StandardCharsets.UTF_8),"reject empty roster");
    rejects("<foo/>".getBytes(StandardCharsets.UTF_8),"reject wrong document");
    rejects(("<!DOCTYPE Workbook [<!ENTITY xx SYSTEM \"file:///etc/passwd\">]>"+
      "<Workbook><Row><Data>ID.: 1 Name: &xx; Dept.Name: Sector</Data></Row></Workbook>")
      .getBytes(StandardCharsets.UTF_8),"reject DTD and local file inclusion");
    byte[] large=new byte[ClockRosterCore.MAX_INPUT_BYTES+1];
    java.util.Arrays.fill(large,(byte)' ');
    large[0]='<';
    rejects(large,"reject oversized SpreadsheetML import");
    rejects((head+row("ID.: 8 Name:  Dept.Name: Vacío")+tail)
      .getBytes(StandardCharsets.UTF_8),"reject missing name");
    System.out.println("PASS: "+cases+" Excel roster import unit checks, including real SpreadsheetML, duplicates and unsafe input");
  }
}
