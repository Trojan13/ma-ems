package BleBeans;

public class IntensityLockBean extends BaseBean {
    public static final byte COMMAND = 5;

    /* JADX INFO: super call moved to the top of the method (can break code semantics) */
    public IntensityLockBean(boolean z) {
        super((byte) 5, z ? new byte[]{0} : new byte[]{1});
    }

    public IntensityLockBean(byte[] bArr) throws BleDataAnasysException {
        super(bArr);
    }

    public boolean getLockState() {
        byte[] infoByteArray = getInfoByteArray();
        if (infoByteArray == null || infoByteArray.length <= 0 || infoByteArray[0] != 0) {
            return false;
        }
        return true;
    }
}
