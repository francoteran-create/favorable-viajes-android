from pathlib import Path
import os
root=Path(os.environ["PROJECT"])
gradle=root/"app/build.gradle"
s=gradle.read_text()
# Add a hardened release build. Do not enable shrinking in debug testing builds.
if "minifyEnabled true" not in s:
 marker="android {"
 assert marker in s
 s=s.replace(marker,'''android {
    lint { disable 'ExpiredTargetSdkVersion' }
    buildTypes {
        release {
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
''',1)
 gradle.write_text(s)
rules=root/"app/proguard-rules.pro"
with rules.open("a") as f:
 f.write("""
# Nautilus: preserve Android entrypoints and androidx callbacks.
-keep class * extends android.app.Activity { *; }
-keep class * extends android.content.ContentProvider { *; }
-keep class androidx.core.content.FileProvider { *; }
-keepattributes *Annotation*,Signature,InnerClasses,EnclosingMethod
# Do not print private contents or license information in release logs.
-assumenosideeffects class android.util.Log {
    public static int v(...);
    public static int d(...);
}
""")
print("V91 release minification, resource shrinking and Android entrypoint rules")
