package BleBeans;


public class DeviceStateReadBean extends BaseBean {
    public static final byte COMMAND = 7;
    private static final byte[] info = {0};

    public DeviceStateReadBean() {
        super((byte) 7, info);
    }

    public DeviceStateReadBean(byte[] bArr) throws BleDataAnasysException {
        super(bArr);
    }

    public DeviceState getDeviceState() {
        byte[] infoByteArray = getInfoByteArray();
        if (infoByteArray == null || infoByteArray.length <= 8) {
            return null;
        }
        return new DeviceState(infoByteArray);
    }
}
