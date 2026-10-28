"""Return the center of an Android UI node with exact visible text."""
import re
import sys
import xml.etree.ElementTree as ET

if len(sys.argv)!=3:
    raise SystemExit("usage: ci_android_tap.py <xml> <visible text>")
root=ET.parse(sys.argv[1]).getroot()
for element in root.iter("node"):
    if element.attrib.get("text")==sys.argv[2]:
        m=re.fullmatch(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]",element.attrib.get("bounds",""))
        if not m:
            raise SystemExit("UI node has no valid bounds")
        x1,y1,x2,y2=map(int,m.groups())
        if x1>=x2 or y1>=y2:
            raise SystemExit("Invalid UI node dimensions")
        print((x1+x2)//2,(y1+y2)//2)
        sys.exit(0)
raise SystemExit("UI item not found: "+sys.argv[2])
