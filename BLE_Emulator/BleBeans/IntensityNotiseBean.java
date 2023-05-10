package BleBeans;


public class IntensityNotiseBean extends BaseBean {
    public static final byte COMMAND = 11;
    private static final byte[] info = {0};

    public IntensityNotiseBean() {
        super(COMMAND, info);
    }

    public IntensityNotiseBean(byte[] bArr) {
        super(bArr);
    }

    public int getIntensity() {
        byte[] infoByteArray = getInfoByteArray();
        if (infoByteArray == null || infoByteArray.length <= 0) {
            return -1;
        }
        return infoByteArray[0];
    }
}
