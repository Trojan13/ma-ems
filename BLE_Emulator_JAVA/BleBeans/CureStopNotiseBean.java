package BleBeans;

public class CureStopNotiseBean extends BaseBean {
    public static final byte COMMAND = 12;
    private static final byte[] info = {0};

    public CureStopNotiseBean() {
        super(COMMAND, info);
    }

    public CureStopNotiseBean(byte[] bArr)  {
        super(bArr);
    }
}
