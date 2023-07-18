# main.py

import asyncio
import platform
import sys
import keyboard  # install with pip install keyboard

from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError
from BLEDeviceState import BLEDeviceState

ADDRESS = "F9:8B:6F:12:EC:AE"
CHARACTERISTICS = "64668730-033f-9393-6ca2-0e9401adeb32"
currentDeviceState = None


async def get_device_info(client, currentDeviceState):
    while True:
        await asyncio.sleep(0.1)  # Pause for 1 second
        #await client.write_gatt_char(CHARACTERISTICS,  bytearray([0x5a, 0x05, 0x07, 0x00, 0x00, 0x66]), True)
        if keyboard.is_pressed('v'):  # if key 'a' is pressed
            print('Add')
            await client.write_gatt_char(CHARACTERISTICS, bytearray(
                [0x5a, 0x05, 0x01, 0x00, 0x00, 0x60]), True)
        elif keyboard.is_pressed('b'):  # if key 'b' is pressed
            print('Decr')
            await client.write_gatt_char(CHARACTERISTICS, bytearray([0x5a, 0x05, 0x02, 0x00, 0x00, 0x61]), True)


def device_state_notify_handler(sender, data):
    print("notify: {0}".format(list(data)))
    print(BLEDeviceState(list(data)))


async def main(ble_address: str):
    device = await BleakScanner.find_device_by_address(ble_address, timeout=20.0)
    if not device:
        raise BleakError(
            f"A device with address {ble_address} could not be found.")
    async with BleakClient(device) as client:
        await client.start_notify(CHARACTERISTICS, device_state_notify_handler)

        await asyncio.sleep(1.0)
        print("sendin")
        # wooooorks await client.write_gatt_char(CHARACTERISTICS, b'\x5a\x05\x01\x00\x00\x60',True)
        # await client.write_gatt_char(CHARACTERISTICS, bytearray([0x5a, 0x05, 0x01, 0x00, 0x00, 0x60]),True)
        # await client.write_gatt_char(CHARACTERISTICS, bytearray([0x5a, 0x05, 0x02, 0x00, 0x00, 0x61]),True)

        # Create the background task
        get_device_info_task = asyncio.create_task(
            get_device_info(client, currentDeviceState))

        # Wait for the background task to complete
        await get_device_info_task


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) == 2 else ADDRESS))
