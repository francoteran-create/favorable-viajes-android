package ar.com.nautiluscountry.presentismo;

import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;

public final class ClockPunchCoreTest {
  private static int checks;
  private static void check(boolean condition,String name){
    ++checks;if(!condition)throw new AssertionError(name);
  }
  private static String head(){return "<?xml version=\"1.0\"?><Workbook xmlns=\"urn:schemas-microsoft-com:office:spreadsheet\" "+
    "xmlns:ss=\"urn:schemas-microsoft-com:office:spreadsheet\"><Worksheet><Table>";}
  private static String tail(){return "</Table></Worksheet></Workbook>";}
  private static String row(String... cols){
    StringBuilder b=new StringBuilder("<Row>");
    for(String s:cols)b.append("<Cell><Data ss:Type=\"String\">").append(s).append("</Data></Cell>");
    return b.append("</Row>").toString();
  }
  private static ArrayList<ClockPunchCore.Punch> parse(String text)throws Exception{
    return ClockPunchCore.parse(new ByteArrayInputStream(text.getBytes(StandardCharsets.UTF_8)));
  }
  private static void reject(byte[] data,String description)throws Exception{
    boolean threw=false;
    try{ClockPunchCore.parse(new ByteArrayInputStream(data));}
    catch(Exception expected){threw=true;}
    check(threw,description);
  }
  public static void main(String[] args)throws Exception{
    String headers=row("ID.","Name","Att.Time","Device ID");
    String fixture=head()+headers+
      row("0007","Ana Pérez","2026-10-28T07:59:00","Clock-A")+
      row("42","Pedro","2026-10-28 18:01:08","Clock-B")+
      row("42","Pedro","28/10/2026 18:01","Clock-B")+tail();
    ArrayList<ClockPunchCore.Punch> found=parse(fixture);
    check(found.size()==3,"all three timestamp formats accepted");
    check(found.get(0).id.equals("0007"),"leading-zero employee ID preserved");
    check(found.get(0).stamp.equals("2026-10-28T07:59:00"),"T timestamp");
    check(found.get(1).stamp.equals("2026-10-28T18:01:08"),"space timestamp");
    check(found.get(2).stamp.equals("2026-10-28T18:01:00"),"Argentine date and missing seconds");
    check(found.get(0).name.equals("Ana Pérez"),"employee name preserved");
    check(found.get(0).device.equals("Clock-A"),"device field preserved");
    String sparse="<Row><Cell ss:Index=\"2\"><Data ss:Type=\"String\">ID.</Data></Cell>"+
      "<Cell><Data>Name</Data></Cell><Cell><Data>Att.Time</Data></Cell></Row>";
    String data="<Row><Cell ss:Index=\"2\"><Data>0010</Data></Cell>"+
      "<Cell><Data>María</Data></Cell><Cell><Data>2026/10/28 06:30:00</Data></Cell></Row>";
    ArrayList<ClockPunchCore.Punch> parsed=parse(head()+row("REPORTE DE ASISTENCIA")+
      sparse+data+tail());
    check(parsed.size()==1,"find header after title, sparse ss:Index");
    check(parsed.get(0).stamp.equals("2026-10-28T06:30:00"),"slash timestamp");
    check(parse(head()+headers+row("7","Ana","2026-10-28 08:00:00","")+
      row("7","Ana","2026-10-28 08:00:00","")+tail()).size()==2,
      "duplicates preserved for SQLite unique index");
    check(parse(head()+headers+row("bad id","Ana","2026-10-28 08:00:00","")+
      row("7","Ana","2026-10-28 08:00:00","")+tail()).size()==1,
      "bad ID ignored");
    reject((head()+headers+row("1","A","2026-02-30 08:00:00","")+tail())
      .getBytes(StandardCharsets.UTF_8),"invalid calendar date rejected");
    reject((head()+headers+row("1","A","2026-10-28 25:00:00","")+tail())
      .getBytes(StandardCharsets.UTF_8),"invalid clock hour rejected");
    reject((head()+row("name","time")+tail()).getBytes(StandardCharsets.UTF_8),
      "missing headers rejected");
    reject(new byte[]{(byte)0xd0,(byte)0xcf,0x11,(byte)0xe0},"binary .xls rejected");
    reject(new byte[]{'P','K',3,4},"binary .xlsx rejected");
    reject(("<!DOCTYPE Workbook [<!ENTITY x SYSTEM \"file:///etc/passwd\">]>"+
      "<Workbook><Row><Cell><Data>&x;</Data></Cell></Row></Workbook>")
      .getBytes(StandardCharsets.UTF_8),"external entity rejected");
    byte[] huge=new byte[ClockPunchCore.MAX_INPUT_BYTES+1];
    Arrays.fill(huge,(byte)' ');
    reject(huge,"oversize import rejected");
    System.out.println("PASS: "+checks+" biometric clock punch tests, timestamps, sparse cells and malformed input");
  }
}
