package BleBeans;



public class EletricOverLoadNotiseBean extends BaseBean {
    public static final byte COMMAND = 14;
    private static final byte[] info = {0};

    public EletricOverLoadNotiseBean() {
        super(COMMAND, info);
    }

    public EletricOverLoadNotiseBean(byte[] bArr) throws BleDataAnasysException {
        super(bArr);
    }
}
