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

        await asyncio.sleep(1)
        device_state = bytes(await client.read_gatt_char(READ_SERVICE))
        print("device_state: {0}".format(device_state))

        t = await client.write_gatt_char(WRITE_SERVICE,  bytearray(intensityAdd))
        print(t)
        await asyncio.sleep(1.0)

 
        print("start brute force")
        for byte1 in range(256):
            for byte2 in range(256):
                for byte3 in range(256):
                    for byte4 in range(256):
                        byteArray = [0x5a, 0x05, byte1, byte2, byte3, byte4]
                        print("sending: {0}".format(byteArray))
                        await client.write_gatt_char(WRITE_SERVICE, bytearray(byteArray))
                        await asyncio.sleep(0.2)

        print("Finish!")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) == 2 else ADDRESS))
