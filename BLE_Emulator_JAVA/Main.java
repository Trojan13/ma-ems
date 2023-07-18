

import BleBeans.BaseBean;
import BleBeans.IntensityLockBean;
import BleBeans.IntensityNotiseBean;
import BleBeans.IntensitySetBean;

import java.util.Arrays;

//BaseBean baseBean2 = new BaseBean(data);
//System.out.println(Arrays.toString(baseBean2.getAllByte()));
public class Main {
    public static void main(String[] args) {
        // create a BleBeans.BaseBean object with a command byte and an info byte array
        System.out.println("Startup....");
        LT1102SBleBean testBean = new LT1102SBleBean("F9:8B:6F:12:EC:AE");

        byte[] bArr = {0x5A, 0x05, 0x0B, 0x04, 0x00, 0x6E};
        BaseBean testBaseBean = new BaseBean(bArr);
        System.out.println(testBaseBean.getCommandByte());

        IntensityNotiseBean testIntensityNotiseBean = new IntensityNotiseBean(bArr);
        System.out.println(testIntensityNotiseBean.getIntensity());
        new IntensityLockBean(true).printAllByte();
        new IntensitySetBean(5).printAllByte();

        // create a BleBeans.BaseBean object with a byte array
        byte[] data = {42, 7, 2, 1, 2, 3, 4, -6, -1};
        try {
            System.out.println("Testing....");


            //testBean.createBleNotifyBean(data);
            byte[] testByteArray = testBean.intensityAdd();
            System.out.println(HexUtil.formatHexString(testByteArray,true));
            System.out.println(HexUtil.formatHexString(testByteArray,true));

            /*
            testBean.intensityCut();
            testBean.setIntensityLock();
            testBean.readDeviceState();
            testBean.setPrgram(1337);
             */
        } catch (Error e) {
            e.printStackTrace();
        }
    }
}