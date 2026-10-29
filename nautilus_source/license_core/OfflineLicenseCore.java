package ar.com.nautiluscountry.presentismo;

import java.nio.charset.StandardCharsets;
import java.security.PublicKey;
import java.security.Signature;
import java.util.Calendar;
import java.util.TimeZone;

/**
 * Pure Java logic shared by the Android license gate and its automated tests.
 * Does not contain, recover or create the owner's private signing key.
 */
public final class OfflineLicenseCore {
  private static final TimeZone ARGENTINA = TimeZone.getTimeZone("America/Argentina/Buenos_Aires");
  private OfflineLicenseCore() {}

  public static long today(long now) {
    Calendar c = Calendar.getInstance(ARGENTINA);
    c.setTimeInMillis(now);
    return c.get(Calendar.YEAR)*10000L + (c.get(Calendar.MONTH)+1)*100L + c.get(Calendar.DAY_OF_MONTH);
  }

  /** Three calendar months from activation, in Argentine civil time. */
  public static long addMonths(long activation) {
    Calendar c = Calendar.getInstance(ARGENTINA);
    c.setTimeInMillis(activation);
    c.add(Calendar.MONTH, 3);
    return c.getTimeInMillis();
  }

  public static byte[] payload(long issuedDay, String nonce) {
    if (!validNonce(nonce) || issuedDay < 20210101L || issuedDay > 21001231L) {
      throw new IllegalArgumentException("Invalid license metadata");
    }
    return ("NTL86:" + issuedDay + ":" + nonce).getBytes(StandardCharsets.UTF_8);
  }

  private static boolean validNonce(String s) {
    return s != null && s.matches("[A-Za-z0-9_-]{12,64}");
  }

  /** Returns a safe nonce only after signature and date verification; null means invalid. */
  public static String verify(byte[] payload, byte[] signature, PublicKey publicKey, long localDay) {
    try {
      if (payload == null || signature == null || publicKey == null ||
          payload.length < 26 || payload.length > 90 || signature.length != 256) return null;
      Signature verifier = Signature.getInstance("SHA256withRSA");
      verifier.initVerify(publicKey);
      verifier.update(payload);
      if (!verifier.verify(signature)) return null;
      String value = new String(payload, StandardCharsets.UTF_8);
      String[] fields = value.split(":", -1);
      if (fields.length != 3 || !"NTL86".equals(fields[0]) ||
          !fields[1].matches("[0-9]{8}") || !validNonce(fields[2])) return null;
      if (Long.parseLong(fields[1]) != localDay) return null;
      byte[] canonical = payload(localDay, fields[2]);
      if (!java.security.MessageDigest.isEqual(canonical, payload)) return null;
      return fields[2];
    } catch (Exception invalid) {
      return null;
    }
  }
}
