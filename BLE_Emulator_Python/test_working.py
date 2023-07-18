import asyncio
import platform
import sys

from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError


ADDRESS = "F9:8B:6F:12:EC:AE"
CHARACTERISTICS = "64668730-033f-9393-6ca2-0e9401adeb32"
currentDeviceState = []


def device_state_notify_handler(sender, data):
    currentDeviceState = list(data)
    print("Notify: {0}".format(list(data)))


async def main(ble_address: str):
    device = await BleakScanner.find_device_by_address(ble_address, timeout=20.0)
    if not device:
        raise BleakError(
            f"A device with address {ble_address} could not be found.")
    async with BleakClient(device) as client:
        await client.start_notify(CHARACTERISTICS, device_state_notify_handler)

        await asyncio.sleep(5.0)
        device_state = bytes(await client.read_gatt_char(CHARACTERISTICS))
        print("device_state: {0}".format(list(device_state)))
        await asyncio.sleep(5.0)

        print("setIntensity lol")
        t = await client.write_gatt_char(CHARACTERISTICS,  bytearray(intensityAdd))
        print(t)
        await asyncio.sleep(1.0)

        print("Finish!")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) == 2 else ADDRESS))
