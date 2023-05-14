# main.py

import asyncio
import sys

from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError
from BLEDeviceState import BLEDeviceState
from BLEDeviceState import BLEDeviceState
from EMSCommand import EMSCommand
from EMSConnectionState import EMSConnectionState
from generate_packet import generate_packet



DEBUG = True
ADDRESS = "F9:8B:6F:12:EC:AE"
CHARACTERISTICS = "64668730-033f-9393-6ca2-0e9401adeb32"


async def get_device_info(client):
    await client.write_gatt_char(CHARACTERISTICS,  generate_packet(EMSCommand.SET_INTENSITY, [0x00])), True)


def device_state_notify_handler(sender, data):
    if DEBUG:
        print("notify: {0}".format(list(data)))
        print(BLEDeviceState(list(data)))

async def register_notification(client):
    await client.start_notify(CHARACTERISTICS, device_state_notify_handler)
    

async def connect():
    device = await BleakScanner.find_device_by_address(ADDRESS, timeout=20.0)
    if not device:
        raise BleakError(
            f"A device with address {ADDRESS} could not be found.")
    async with BleakClient(device) as client:
        if client.is_connected:
            connection_state = EMSConnectionState.BLE_STATE_CONNECT_CONNECTED
            print(f"Connected: {connection_state}")
        else:
            connection_state = EMSConnectionState.BLE_STATE_CONNECT_CONNECT_FAIL
            print(f"Failed to connect: {connection_state}")

    if not client.is_connected:
        connection_state = EMSConnectionState.BLE_STATE_CONNECT_DISCONNECTED
        print(f"Disconnected: {connection_state}")
    
    # Registers the device state notify handler to read the device state
    await register_notification(client)
    # Sends a packet to the EMS device to read the device state
    get_device_info(client)


if __name__ == "__main__":
    asyncio.run(connect(ADDRESS))
