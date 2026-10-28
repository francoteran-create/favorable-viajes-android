from pathlib import Path
import os
p=Path(os.environ["PROJECT"])/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
start=s.index(" int importPersonnelReport(InputStream in)throws Exception{")
marker="  ensurePersonnelMaster();SQLiteDatabase w=db.getWritableDatabase();"
end=s.index(marker,start)
new=''' int importPersonnelReport(InputStream in)throws Exception{
  // Canonical, unit-tested XML Spreadsheet 2003 report parser.
  // Reads the original clock IDs; does not infer shifts from punches.
  java.util.LinkedHashMap<String,String[]> found=ClockRosterCore.parse(in);
'''
s=s[:start]+new+s[end:]
p.write_text(s)
core=Path(__file__).with_name("excel_core")/"ClockRosterCore.java"
out=p.with_name("ClockRosterCore.java")
out.write_bytes(core.read_bytes())
print("V109: protected XLS SpreadsheetML roster parser integrated into Android importer")
