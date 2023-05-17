import asyncio
import websockets
import sys
import logging
import json

from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError

from EM70 import DeviceState, Command, ConnectionState, generate_packet, validate_packet

ADDRESS = "F9:8B:6F:12:EC:AE"
CHARACTERISTICS = "64668730-033f-9393-6ca2-0e9401adeb32"
ble_client = None  # Global BLE client
ws_client = None  # Global WebSocket client
ws_server = None  # Global WebSocket server

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.INFO)


async def device_state_notify_handler(sender, data):
    device_state = DeviceState(list(data))
    logging.info("notify: {0}".format(list(data)))

    if ws_client and ws_client.open:
        await ws_client.send(device_state.get_json())


async def get_device_info(client):
    while client.is_connected:
        await client.write_gatt_char(CHARACTERISTICS, generate_packet(Command.DEVICE_STATE_READ, [0x00]), True)
        await asyncio.sleep(1)


async def connect_ble(ble_address: str):
    global ble_client
    logging.info("Trying to connect BLE...")
    device = await BleakScanner.find_device_by_address(ble_address, timeout=20.0)
    if not device:
        raise BleakError(
            f"A device with address {ble_address} could not be found.")

    ble_client = BleakClient(device)
    await ble_client.connect()
    await ble_client.start_notify(CHARACTERISTICS, device_state_notify_handler)


async def connect_ws():
    global ws_server
    logging.info("Starting WS server...")
    ws_server = await websockets.serve(websocket_handler, "localhost", 8765)


async def websocket_handler(websocket, path):
    global ws_client
    ws_client = websocket
    logging.info("WS Client connected...")

    while True:
        if not ws_client.open:
            logging.info("WS Client disconnected...")
            break

        msg = await websocket.recv()

        if ble_client and ble_client.is_connected:
            print(msg)
            print(validate_packet(msg))
            if validate_packet(msg):
                await ble_client.write_gatt_char(CHARACTERISTICS, bytes.fromhex(msg), True)
            else:
                try:
                    msg_json = json.loads(msg)
                    command = msg_json.get('command', None)
                    if command == 'pause':
                        await ble_client.write_gatt_char(CHARACTERISTICS, generate_packet(Command.PROGRAM_PAUSE, [0x00]), True)
                    elif command == 'add':
                        await ble_client.write_gatt_char(CHARACTERISTICS, generate_packet(Command.INTENSITY_ADD, [0x00]), True)
                    elif command == 'cut':
                        await ble_client.write_gatt_char(CHARACTERISTICS, generate_packet(Command.INTENSITY_CUT, [0x00]), True)
                    elif command == 'seti':
                        intensity = int(msg_json.get('value', 0))
                        await ble_client.write_gatt_char(CHARACTERISTICS, generate_packet(Command.INTENSITY_SET, [intensity]), True)
                except Exception as e:
                    logging.error(e)
        else:
            logging.info("BLE client not connected yet")

        if not ws_client.open:
            logging.info("WS Client disconnected...")
            break


async def main():
    while True:
        if not ws_server:
            try:
                await connect_ws()
            except Exception as e:
                logging.error(e)
                await asyncio.sleep(5)

        if not ble_client or not ble_client.is_connected:
            try:
                await connect_ble(ADDRESS)
                asyncio.create_task(get_device_info(ble_client))
            except Exception as e:
                logging.error(e)
                await asyncio.sleep(5)

        await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
