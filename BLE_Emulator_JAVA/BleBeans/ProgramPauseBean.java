package BleBeans;

public class ProgramPauseBean extends BaseBean {
    public static final byte COMMAND = 6;

    /* JADX INFO: super call moved to the top of the method (can break code semantics) */
    public ProgramPauseBean(boolean z) {
        super((byte) 6, z ? new byte[]{0} : new byte[]{1});
    }

    public boolean getPauseState() {
        byte[] infoByteArray = getInfoByteArray();
        if (infoByteArray == null || infoByteArray.length <= 0 || infoByteArray[0] != 0) {
            return false;
        }
        return true;
    }
}
