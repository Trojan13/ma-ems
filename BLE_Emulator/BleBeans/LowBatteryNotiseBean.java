package BleBeans;


public class LowBatteryNotiseBean extends BaseBean {
    public static final byte COMMAND = 15;
    private static final byte[] info = {0};

    public LowBatteryNotiseBean() {
        super(COMMAND, info);
    }

    public LowBatteryNotiseBean(byte[] bArr) throws BleDataAnasysException {
        super(bArr);
    }
}
