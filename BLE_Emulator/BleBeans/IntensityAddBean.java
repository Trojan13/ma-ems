package BleBeans;

public class IntensityAddBean extends BaseBean {
    public static final byte COMMAND = 1;
    private static final byte[] info = {0};

    public IntensityAddBean() {
        super((byte) 1, info);
    }

    public int getIntensity() {
        byte[] infoByteArray = getInfoByteArray();
        if (infoByteArray == null || infoByteArray.length <= 0) {
            return -1;
        }
        return infoByteArray[0];
    }
}
