package BleBeans;

public class ShutdownBean extends BaseBean {
    public static final byte COMMAND = 13;
    private static final byte[] info = {0};

    public ShutdownBean() {
        super(COMMAND, info);
    }
}
