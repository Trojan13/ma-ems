package BleBeans;

public class VersionReadBean extends BaseBean {
    public static final byte COMMAND = 8;
    private static final byte[] info = {0};

    public VersionReadBean() {
        super((byte) 8, info);
    }

    public int getHardwareVersion() {
        byte[] infoByteArray = getInfoByteArray();
        if (infoByteArray == null || infoByteArray.length <= 0) {
            return -1;
        }
        return infoByteArray[0];
    }

    public int getSoftwareVersion() {
        byte[] infoByteArray = getInfoByteArray();
        if (infoByteArray == null || infoByteArray.length <= 1) {
            return -1;
        }
        return infoByteArray[1];
    }
}
