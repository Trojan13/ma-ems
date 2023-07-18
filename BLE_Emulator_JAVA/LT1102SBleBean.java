import BleBeans.DeviceState;
import BleBeans.NotifyType;
import BleBeans.BaseBean;
import BleBeans.CureStopNotiseBean;
import BleBeans.DeviceStateReadBean;
import BleBeans.EletricOverLoadNotiseBean;
import BleBeans.IntensityAddBean;
import BleBeans.IntensityCutBean;
import BleBeans.IntensityLockBean;
import BleBeans.IntensityNotiseBean;
import BleBeans.IntensitySetBean;
import BleBeans.LowBatteryNotiseBean;
import BleBeans.ProgramSetBean;
import BleBeans.ShutdownBean;
import BleBeans.BleDataAnasysException;
import BleBeans.BleException;
import BleBeans.BleWriteCallback;

import java.util.Objects;
import java.util.Arrays;

public class LT1102SBleBean {
    public static final int BLE_STATE_CONNECT_CONNECTED = 2;
    public static final int BLE_STATE_CONNECT_CONNECTING = 1;
    public static final int BLE_STATE_CONNECT_CONNECT_FAIL = 3;
    public static final int BLE_STATE_CONNECT_DISCONNECTED = 4;
    public static final int BLE_STATE_CONNECT_NONE = 0;
    private int mDeviceConnectSate = 0;
    private DeviceState mDeviceState;
    private String mac = "";

    public LT1102SBleBean(String mac) {
        this.mac = mac;
    }

    public void createBleNotifyBean(byte[] bArr) {
        try {
            BaseBean baseBean = new BaseBean(bArr);
            System.out.println("Notify:" + baseBean.getCommandByte());
            byte commandByte = baseBean.getCommandByte();
            if (commandByte == 4) {
                ProgramSetBean programSetBean = new ProgramSetBean(bArr);
                System.out.println(NotifyType.PROGRAM);
                System.out.println(programSetBean.getProgram());
            } else if (commandByte == 5) {
                IntensityLockBean intensityLockBean = new IntensityLockBean(bArr);
                System.out.println(NotifyType.LOCK);
                //deviceState2.setIntensityLock(intensityLockBean.getLockState());
            } else if (commandByte == 7) {
                // this.mDeviceState = new DeviceStateReadBean(bArr).getDeviceState();
                System.out.println(NotifyType.ALL_STATE);
            } else if (commandByte == 11) {
                // IntensityNotiseBean intensityNotiseBean = new IntensityNotiseBean(bArr);
                // deviceState3.setIntensity(intensityNotiseBean.getIntensity());
                System.out.println(NotifyType.INTENSITY);
            } else if (commandByte == 12) {
                //new CureStopNotiseBean(bArr);
                // deviceState4.setCureState(0);
                System.out.println(NotifyType.CURE_STOP);
            } else if (commandByte == 14) {
                //new EletricOverLoadNotiseBean(bArr);
                //  deviceState5.setElectriyOverLoad(true);
                System.out.println(NotifyType.OVERLOAD);
            } else if (commandByte == 15) {
                //new LowBatteryNotiseBean(bArr);
                //  deviceState6.setBattery(0);
                System.out.println(NotifyType.LOW_BATTERY);
            }
        } catch (BleDataAnasysException e) {
            System.out.println(e.getMessage());
        }
    }

    public byte[] intensityAdd() {
        System.out.print("intensityAdd: ");
        IntensityAddBean TestIntensityAddBean = new IntensityAddBean();
        TestIntensityAddBean.printAllByte();

        BaseBean TestBaseBean = new BaseBean(TestIntensityAddBean.getCommandByte(),TestIntensityAddBean.getInfoByteArray());
        TestBaseBean.printAllByte();
        return TestIntensityAddBean.getAllByte();
    }

    public void intensityCut() {
        System.out.print("IntensityCutBean: ");
        new IntensityCutBean().printAllByte();

        if (this.mDeviceState == null) {
            //onDeviceSetListener.onSetResult(false);
        } else {
            writeToBle(new IntensityAddBean().getAllByte(), new BleWriteCallback() {
                public void onWriteSuccess(int i, int i2, byte[] bArr) {
                    //onDeviceSetListener.onSetResult(true);
                }

                public void onWriteFailure(BleException bleException) {
                    // onDeviceSetListener.onSetResult(false);
                }
            });
        }
    }

    public void setIntensityLock() {
        System.out.print("setIntensityLock: ");
        new IntensityLockBean(true).printAllByte();
        System.out.print("setIntensity: ");
        new IntensitySetBean(0).printAllByte();

        if (this.mDeviceState == null) {
            // onDeviceSetListener.onSetResult(false);
        } else {
            writeToBle(new IntensityLockBean(!this.mDeviceState.isIntensityLock()).getAllByte(), new BleWriteCallback() {
                public void onWriteSuccess(int i, int i2, byte[] bArr) {
                    // onDeviceSetListener.onSetResult(true);
                }

                public void onWriteFailure(BleException bleException) {
                    // onDeviceSetListener.onSetResult(false);
                }
            });
        }
    }

    public void stopCure() {
        if (this.mDeviceState == null) {
            //  onDeviceSetListener.onSetResult(false);
        } else {
            writeToBle(new IntensitySetBean(0).getAllByte(), new BleWriteCallback() {
                public void onWriteSuccess(int i, int i2, byte[] bArr) {
                    //   onDeviceSetListener.onSetResult(true);
                }

                public void onWriteFailure(BleException bleException) {
                    //    onDeviceSetListener.onSetResult(false);
                }
            });
        }
    }

    public void readDeviceState() {
        System.out.print("readDeviceState: ");
        new DeviceStateReadBean().printAllByte();
        writeToBle(new DeviceStateReadBean().getAllByte(), new BleWriteCallback() {
            public void onWriteSuccess(int i, int i2, byte[] bArr) {
                // OnDeviceSetListener onDeviceSetListener = onDeviceSetListener;
                //  onDeviceSetListener.onSetResult(true);
            }

            public void onWriteFailure(BleException bleException) {
                //  OnDeviceSetListener onDeviceSetListener = onDeviceSetListener;
                //     onDeviceSetListener.onSetResult(false);
            }
        });
    }

    public void deviceClose() {
        if (this.mDeviceState == null) {
            // onDeviceSetListener.onSetResult(false);
        } else {
            writeToBle(new ShutdownBean().getAllByte(), new BleWriteCallback() {
                public void onWriteSuccess(int i, int i2, byte[] bArr) {
                    // onDeviceSetListener.onSetResult(true);
                }

                public void onWriteFailure(BleException bleException) {
                    // onDeviceSetListener.onSetResult(false);
                }
            });
        }
    }

    public void setPrgram(int i) {
        System.out.print("setPrgram: ");
        new ProgramSetBean(i).printAllByte();
        if (this.mDeviceState == null) {
            // onDeviceSetListener.onSetResult(false);
        } else {
            writeToBle(new ProgramSetBean(i).getAllByte(), new BleWriteCallback() {
                public void onWriteSuccess(int i, int i2, byte[] bArr) {
                    //  onDeviceSetListener.onSetResult(true);
                }

                public void onWriteFailure(BleException bleException) {
                    //  onDeviceSetListener.onSetResult(false);
                }
            });
        }
    }

    private void writeToBle(byte[] bArr, BleWriteCallback bleWriteCallback) {
        //MyBleManager.getInstance(MyApplication.getContext()).writeMessage(this.mBleDevice, Constants.SERVICE_UUID, Constants.CHARACTERISTIC_UUID, bArr, bleWriteCallback);
    }

    private void notifyFromBle() {
        // MyBleManager.getInstance(MyApplication.getContext()).receiveMessage(this.mBleDevice, Constants.SERVICE_UUID, Constants.CHARACTERISTIC_UUID, bleNotifyCallback);
    }
}
