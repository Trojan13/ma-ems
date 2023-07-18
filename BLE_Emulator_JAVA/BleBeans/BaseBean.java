package BleBeans;

import java.lang.reflect.Array;
import java.util.Arrays;

public class BaseBean {
    private byte[] checksumByte = new byte[2];
    private byte commandByte;
    private byte[] infoByteArray;
    private byte lengthByte;
    private final byte startByte = 90;

    public BaseBean(byte b, byte[] bArr) {
        this.commandByte = b;
        this.infoByteArray = bArr;
    }

    public byte getCommandByte() {
        return this.commandByte;
    }

    /* access modifiers changed from: protected */
    public byte[] getInfoByteArray() {
        return this.infoByteArray;
    }

    public BaseBean(byte[] bArr) throws Error {
        int length = bArr.length;
        if (length < 5 || bArr[0] != 90) {
            throw new Error("not lt1102s datas");
        }
        byte b = bArr[1];
        this.lengthByte = b;
        this.commandByte = bArr[2];
        int i = b - 4;
        this.infoByteArray = new byte[i];
        for (int i2 = 0; i2 < i; i2++) {
            this.infoByteArray[i2] = bArr[i2 + 3];
        }
        initCheckSum();
        byte[] bArr2 = this.checksumByte;
        if (bArr2[0] != bArr[length - 2] || bArr2[1] != bArr[length - 1]) {
            throw new Error("checksum error");
        }
    }

    public String byteArrayToString(byte[] bArr) {
        String str = "";
        for (int i = 0; i < bArr.length; i++) {
            str = str + Integer.toHexString(bArr[i] & 255) + "  ";
        }
        return str;
    }


    public byte[] getAllByte() {
        int length = this.infoByteArray.length + 5;
        byte[] bArr = new byte[length];
        bArr[0] = 90;
        bArr[1] = this.lengthByte;
        bArr[2] = this.commandByte;
        int i = 0;
        while (true) {
            byte[] bArr2 = this.infoByteArray;
            if (i < bArr2.length) {
                bArr[i + 3] = bArr2[i];
                i++;
            } else {
                byte[] bArr3 = this.checksumByte;
                bArr[length - 2] = bArr3[0];
                bArr[length - 1] = bArr3[1];
                return bArr;
            }
        }
    }

    public void printAllByte(){
        byte[] byteArray = getAllByte();
        for (byte b : byteArray) {
            System.out.print(String.format("%02X ", b));
        }
        System.out.println(Arrays.toString(byteArray));

        System.out.println();
    }

    public int getLength() {
        return getAllByte().length;
    }

    private void initCheckSum() {
        int i = 90 + (this.lengthByte & 255) + (this.commandByte & 255);
        byte[] bArr = this.infoByteArray;
        if (bArr != null) {
            for (byte b : bArr) {
                i += b & 255;
            }
        }
        byte[] bArr2 = this.checksumByte;
        bArr2[0] = (byte) ((i >> 8) & 255);
        bArr2[1] = (byte) (i & 255);
    }
}
