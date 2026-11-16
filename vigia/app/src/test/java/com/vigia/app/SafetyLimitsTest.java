package com.vigia.app;
import org.junit.Test;
import static org.junit.Assert.*;
public class SafetyLimitsTest {
 private static long mb(long value){return value*1024L*1024L;}
 @Test public void normalAboveWarningLimits(){assertEquals(SafetyLimits.Mode.NORMAL,SafetyLimits.evaluate(16,mb(251)));}
 @Test public void warningBatteryAt15(){assertEquals(SafetyLimits.Mode.SEGMENT_30_SECONDS,SafetyLimits.evaluate(15,mb(1000)));}
 @Test public void warningStorageBelow250(){assertEquals(SafetyLimits.Mode.SEGMENT_30_SECONDS,SafetyLimits.evaluate(90,mb(249)));}
 @Test public void criticalBatteryAt5(){assertEquals(SafetyLimits.Mode.STOP_AND_FINALIZE,SafetyLimits.evaluate(5,mb(1000)));}
 @Test public void criticalStorageBelow100(){assertEquals(SafetyLimits.Mode.STOP_AND_FINALIZE,SafetyLimits.evaluate(90,mb(99)));}
 @Test public void boundary100MbIsWarning(){assertEquals(SafetyLimits.Mode.SEGMENT_30_SECONDS,SafetyLimits.evaluate(90,mb(100)));}
 @Test public void boundary250MbIsNormal(){assertEquals(SafetyLimits.Mode.NORMAL,SafetyLimits.evaluate(90,mb(250)));}
}
