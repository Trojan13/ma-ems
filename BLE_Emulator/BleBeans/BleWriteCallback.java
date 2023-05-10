package BleBeans;

public abstract class BleWriteCallback extends BleBaseCallback {
    public abstract void onWriteFailure(BleException bleException);

    public abstract void onWriteSuccess(int i, int i2, byte[] bArr);
}
