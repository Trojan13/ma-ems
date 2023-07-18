package BleBeans;

public class IntensitySetBean extends BaseBean {
    public static final byte COMMAND = 3;

    public IntensitySetBean(int i) {
        super((byte) 3, new byte[]{(byte) i});
    }

    public int getIntensity() {
        byte[] infoByteArray = getInfoByteArray();
        if (infoByteArray == null || infoByteArray.length <= 0) {
            return -1;
        }
        return infoByteArray[0];
    }
}
