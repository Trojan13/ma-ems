import asyncio
import platform
import sys

from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError


ADDRESS = "F9:8B:6F:12:EC:AE"
WRITE_SERVICE = "64668730-033f-9393-6ca2-0e9401adeb32"
READ_SERVICE = "64668730-033f-9393-6ca2-0e9401adeb32"


async def main(ble_address: str):
    device = await BleakScanner.find_device_by_address(ble_address, timeout=20.0)
    if not device:
        raise BleakError(
            f"A device with address {ble_address} could not be found.")
    async with BleakClient(device) as client:
        intensityAdd = [0x5a, 0x05, 0x07, 0x00, 0x00, 0x66]
        intensityCutBean = [0x5A, 0x0, 0x2, 0x0, 0x0, 0x0]
        setIntensityLock = [0x5A, 0x0, 0x5, 0x0, 0x0, 0x0]
        setIntensity = [0x5A, 0x05, 0x0B, 0x04, 0x00, 0x6E]
        readDeviceState = [0x5A, 0x0, 0x7, 0x0, 0x0, 0x0]
        setPrgram = [0x5A, 0x0, 0x4, 0x39, 0x0, 0x0]
        await asyncio.sleep(1.0)
        device_state = bytes(await client.read_gatt_char(READ_SERVICE))
        print("device_state: {0}".format(device_state))
        await asyncio.sleep(5.0)

        print("setIntensity lol")
        t = await client.write_gatt_char(WRITE_SERVICE,  bytearray(intensityAdd))
        print(t)
        await asyncio.sleep(1.0)


        print("Finish!")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) == 2 else ADDRESS))
