import asyncio
import websockets
import sys

from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError
from BLEDeviceState import BLEDeviceState
from generate_packet import generate_packet

ADDRESS = "F9:8B:6F:12:EC:AE"
CHARACTERISTICS = "64668730-033f-9393-6ca2-0e9401adeb32"

connected_ws = None

def device_state_notify_handler(sender, data):
    print("notify: {0}".format(list(data)))
    device_state = BLEDeviceState(list(data))
    print(device_state)

    if connected_ws is not None:
        asyncio.ensure_future(connected_ws.send(str(device_state)))

async def get_device_info(client):
    while client.is_connected:
        await client.write_gatt_char(CHARACTERISTICS, generate_packet(7, [0x00]), True)
        await asyncio.sleep(1)

async def main(ble_address: str):
    print("Trying to connect ble...")
    device = await BleakScanner.find_device_by_address(ble_address, timeout=20.0)
    if not device:
        raise BleakError(f"A device with address {ble_address} could not be found.")
    async with BleakClient(device) as client:
        await client.start_notify(CHARACTERISTICS, device_state_notify_handler)
        await get_device_info(client)

async def websocket_handler(websocket, path):
    print("WS Client connected...")
    global connected_ws
    connected_ws = websocket
    await main(ADDRESS)
    while True:
        msg = await websocket.recv()
        print(msg)
        await asyncio.sleep(1)


async def serve_websockets(loop):
    print("Starting ws server...")
    server = await websockets.serve(websocket_handler, "localhost", 8765, loop=loop)
    await server.wait_closed()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(serve_websockets(loop=loop))
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()