package BleBeans;
public class DeviceState {
    private int battery;
    private int cureState;
    private int cureTimeMinute;
    private int cureTimeSecound;
    private boolean electriyOverLoad;
    private int intensity;
    private boolean intensityLock;
    private int mode;
    private int program;

    public DeviceState(byte[] bArr) {
        if (bArr.length >= 9) {
            boolean z = false;
            this.electriyOverLoad = bArr[0] == 0;
            this.program = bArr[1];
            this.mode = bArr[2];
            this.intensity = bArr[3];
            this.cureTimeMinute = bArr[4];
            this.battery = bArr[5];
            this.cureState = bArr[6];
            this.cureTimeSecound = 60 - bArr[7];
            this.intensityLock = bArr[8] == 0 ? true : z;
        }
    }

    public DeviceState setElectriyOverLoad(boolean z) {
        this.electriyOverLoad = z;
        return this;
    }

    public DeviceState setProgram(int i) {
        this.program = i;
        return this;
    }

    public DeviceState setMode(int i) {
        this.mode = i;
        return this;
    }

    public DeviceState setIntensity(int i) {
        this.intensity = i;
        return this;
    }

    public DeviceState setCureTimeMinute(int i) {
        this.cureTimeMinute = i;
        return this;
    }

    public DeviceState setBattery(int i) {
        this.battery = i;
        return this;
    }

    public DeviceState setCureState(int i) {
        this.cureState = i;
        return this;
    }

    public DeviceState setCureTimeSecound(int i) {
        this.cureTimeSecound = i;
        return this;
    }

    public DeviceState setIntensityLock(boolean z) {
        this.intensityLock = z;
        return this;
    }

    public boolean isElectriyOverLoad() {
        return this.electriyOverLoad;
    }

    public int getProgram() {
        return this.program;
    }

    public int getMode() {
        return this.mode;
    }

    public int getIntensity() {
        return this.intensity;
    }

    public int getCureTimeMinute() {
        return this.cureTimeMinute;
    }

    public int getBattery() {
        return this.battery;
    }

    public int getCureState() {
        return this.cureState;
    }

    public int getCureTimeSecound() {
        return this.cureTimeSecound;
    }

    public boolean isIntensityLock() {
        return this.intensityLock;
    }
}
