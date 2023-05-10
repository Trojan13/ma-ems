package BleBeans;

public class ProgramSetBean extends BaseBean {
    public static final byte COMMAND = 4;

    public ProgramSetBean(int i) {
        super((byte) 4, new byte[]{(byte) i});
    }

    public ProgramSetBean(byte[] bArr) throws BleDataAnasysException {
        super(bArr);
    }

    public int getProgram() {
        byte[] infoByteArray = getInfoByteArray();
        if (infoByteArray == null || infoByteArray.length <= 0) {
            return -1;
        }
        return infoByteArray[0];
    }
}
