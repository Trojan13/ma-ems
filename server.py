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
connected_ws = asyncio.Queue()  # Queue of connected websockets
ble_client = None  # Global BLE client

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.INFO)

condition = asyncio.Condition()


async def device_state_notify_handler(sender, data):
    device_state = DeviceState(list(data))
    logging.info("notify: {0}".format(list(data)))

    # If there is a connected websocket, send the device state to it
    async with condition:
        if connected_ws.empty():
            # if there is no connected websocket, just return
            return
        ws = await connected_ws.get()
    asyncio.ensure_future(ws.send(device_state.get_json()))


async def get_device_info(client):
    while client.is_connected:
        await client.write_gatt_char(CHARACTERISTICS, generate_packet(Command.DEVICE_STATE_READ, [0x00]), True)
        await asyncio.sleep(1)


async def main(ble_address: str):
    global ble_client
    while True:
        logging.info("main")
        async with condition:
            if connected_ws.empty():
                # wait for a notification if the queue is empty
                await condition.wait()

        if not ble_client or not ble_client.is_connected:
            try:
                logging.info("Trying to connect ble...")
                device = await BleakScanner.find_device_by_address(ble_address, timeout=20.0)

                if not device:
                    raise BleakError(
                        f"A device with address {ble_address} could not be found.")
                async with BleakClient(device) as client:
                    ble_client = client
                    await ble_client.start_notify(CHARACTERISTICS, device_state_notify_handler)
                    await get_device_info(ble_client)
            except BleakError as e:
                logging.error(e)
                # wait for 5 seconds before trying to reconnect
                await asyncio.sleep(5)


async def websocket_handler(websocket, path):
    logging.info("WS Client connected...")

    async with condition:
        await connected_ws.put(websocket)
        condition.notify()  # notify main that a websocket has been connected

    while True:
        try:
            msg = await asyncio.wait_for(websocket.recv(), timeout=1.0)
        except asyncio.TimeoutError:
            continue
        except websockets.exceptions.ConnectionClosed:
            logging.info("WS Client disconnected...")
            break
        if msg:
            if ble_client and ble_client.is_connected:
                print(validate_packet(msg))
                print(bytes.fromhex(msg))
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
                            await websocket.client.write_gatt_char(CHARACTERISTICS, generate_packet(Command.INTENSITY_CUT, [0x00]), True)
                        elif command == 'seti':
                            intensity = int(msg_json.get('value', 0))
                            await ble_client.write_gatt_char(CHARACTERISTICS, generate_packet(Command.INTENSITY_SET, [intensity]), True)
                    except Exception as e:
                        logging.error(e)
            else:
                logging.info("BLE client not connected yet")
        else:
            logging.info("Received an empty message")


async def serve_websockets(loop):
    logging.info("Starting ws server...")
    server = await websockets.serve(websocket_handler, "localhost", 8765, loop=loop)
    await server.wait_closed()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(main(ADDRESS))
    loop.create_task(serve_websockets(loop=loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
