package BleBeans;

public class IntensityCutBean extends BaseBean {
    public static final byte COMMAND = 2;
    private static final byte[] info = {0};

    public IntensityCutBean() {
        super((byte) 2, info);
    }

    public int getIntensity() {
        byte[] infoByteArray = getInfoByteArray();
        if (infoByteArray == null || infoByteArray.length <= 0) {
            return -1;
        }
        return infoByteArray[0];
    }
}
