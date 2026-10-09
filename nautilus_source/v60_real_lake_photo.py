from pathlib import Path
import os,base64,urllib.request
root=Path(os.environ["PROJECT"])
res=root/"app/src/main/res/drawable-nodpi";res.mkdir(parents=True,exist_ok=True)
dest=res/"nautilus_lake_real.jpg"
# Always provide a valid tiny JPEG fallback so resource compilation is deterministic.
fallback=base64.b64decode("/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAoHBwgHBgoICAgLCgoLDhgQDg0NDh0VFhEYIx8lJCIfIiEmKzcvJik0KSEiMEExNDk7Pj4+JS5ESUM8SDc9Pjv/2wBDAQoLCw4NDhwQEBw7KCIoOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozv/wAARCAACAAIDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAf/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAwT/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCSgKQv/9k=")
dest.write_bytes(fallback)
urls=[
 "https://images.unsplash.com/photo-1607356547206-4b8ff4a410a8?w=1150&q=76&fit=crop&fm=jpg",
 "https://images.unsplash.com/uploads/1413081299023a90cb371/11f44bb7?w=1150&q=76&fit=crop&fm=jpg"
]
for url in urls:
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; NautilusVisualBuild/1.0)","Accept":"image/jpeg"})
  with urllib.request.urlopen(req,timeout=14) as response: data=response.read(1500000)
  if len(data)>10000 and data[:2]==b"\xff\xd8":
   dest.write_bytes(data);print("V60 PHOTO OK",len(data),"bytes",url);break
 except Exception as exc: print("V60 photo source unavailable:",str(exc)[:140])
else: print("V60 offline image fallback, native lake artwork retained")
p=root/"app/src/main/java/ar/com/nautiluscountry/presentismo/MainActivity.java"
s=p.read_text()
mark=' android.graphics.drawable.Drawable mtLake(final boolean dark){'
assert mark in s
code=r'''
 android.graphics.drawable.Drawable mtPhoto(boolean dark){
  try{
   android.graphics.Bitmap bitmap=android.graphics.BitmapFactory.decodeResource(getResources(),R.drawable.nautilus_lake_real);
   if(bitmap==null||bitmap.getWidth()<100)return mtLake(dark);
   android.graphics.drawable.BitmapDrawable bg=new android.graphics.drawable.BitmapDrawable(getResources(),bitmap);
   bg.setGravity(Gravity.FILL);
   android.graphics.drawable.GradientDrawable overlay=new android.graphics.drawable.GradientDrawable(
    android.graphics.drawable.GradientDrawable.Orientation.TOP_BOTTOM,
    dark?new int[]{0x95010C1D,0xB0010A1B}:new int[]{0x44010B1B,0x80030C1A});
   return new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{bg,overlay});
  }catch(Exception e){return mtLake(dark);}
 }
'''
s=s.replace(mark,code+"\n"+mark,1)
s=s.replace('head.setBackground(mtLake(false));','head.setBackground(mtPhoto(false));')
s=s.replace('card.setBackground(major?mtLake(true):mtBg(','card.setBackground(major?mtPhoto(true):mtBg(')
p.write_text(s)
print("V60 photo-backed Nautilus header + TURNOS hero; offline-safe")
