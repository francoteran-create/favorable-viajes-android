package ar.com.nautiluscountry.presentismo;

import java.nio.charset.StandardCharsets;
import java.security.*;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.Arrays;

public class OfflineLicenseCoreTest {
  private static int count;
  private static void check(boolean valid, String label) {
    ++count;
    if (!valid) throw new AssertionError(label);
  }
  private static byte[] sign(PrivateKey key, byte[] message) throws Exception {
    Signature sig=Signature.getInstance("SHA256withRSA");
    sig.initSign(key);sig.update(message);
    return sig.sign();
  }
  private static long argentina(String value) {
    return LocalDateTime.parse(value).atZone(ZoneId.of("America/Argentina/Buenos_Aires"))
        .toInstant().toEpochMilli();
  }
  public static void main(String[] args) throws Exception {
    KeyPairGenerator generator=KeyPairGenerator.getInstance("RSA");
    generator.initialize(2048);
    KeyPair owner=generator.generateKeyPair();
    KeyPair stranger=generator.generateKeyPair();
    long today=20261028L;
    String nonce="abcABC_1234-QRST";
    byte[] payload=OfflineLicenseCore.payload(today,nonce);
    byte[] sig=sign(owner.getPrivate(),payload);
    check(nonce.equals(OfflineLicenseCore.verify(payload,sig,owner.getPublic(),today)),"valid same-day code");
    check(OfflineLicenseCore.verify(payload,sig,owner.getPublic(),today+1)==null,"reject expired issue day");
    check(OfflineLicenseCore.verify(payload,sig,stranger.getPublic(),today)==null,"wrong signing key");
    check(OfflineLicenseCore.verify(payload,sign(stranger.getPrivate(),payload),owner.getPublic(),today)==null,"forged signature");
    byte[] modified=payload.clone();modified[modified.length-1]^=1;
    check(OfflineLicenseCore.verify(modified,sig,owner.getPublic(),today)==null,"modified payload");
    check(OfflineLicenseCore.verify(payload,Arrays.copyOf(sig,10),owner.getPublic(),today)==null,"short signature");
    check(OfflineLicenseCore.verify(null,sig,owner.getPublic(),today)==null,"null payload");
    for(String bad:new String[]{"abc","NTL87:20261028:"+nonce,"NTL86:20261028:x",
        "NTL86:20261028:"+nonce+":OTHER","NTL86:20261028:two words here"}) {
      byte[] b=bad.getBytes(StandardCharsets.UTF_8);
      check(OfflineLicenseCore.verify(b,sign(owner.getPrivate(),b),owner.getPublic(),today)==null,"signed malformed payload "+bad);
    }
    check(OfflineLicenseCore.today(Instant.parse("2026-10-29T02:59:59Z").toEpochMilli())==20261028L,
        "Argentina date before midnight");
    check(OfflineLicenseCore.today(Instant.parse("2026-10-29T03:00:00Z").toEpochMilli())==20261029L,
        "Argentina date after midnight");
    check(OfflineLicenseCore.addMonths(argentina("2024-01-31T10:30:00"))==
        argentina("2024-04-30T10:30:00"),"3 calendar months end-of-month");
    check(OfflineLicenseCore.addMonths(argentina("2024-11-30T10:30:00"))==
        argentina("2025-02-28T10:30:00"),"3 months across year and February");
    check(OfflineLicenseCore.addMonths(argentina("2026-10-28T16:15:00"))==
        argentina("2027-01-28T16:15:00"),"3 months normal");
    boolean rejected=false;
    try {OfflineLicenseCore.payload(today,"short");}catch(IllegalArgumentException expected){rejected=true;}
    check(rejected,"nonce length enforcement");
    System.out.println("PASS: "+count+" offline licensing unit checks (RSA, date, expiry, tampering)");
  }
}
