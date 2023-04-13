import asyncio
import uuid
import logging
from  bleak import BleakClient, BleakScanner

address = "F9:8B:6F:12:EC:AE"
DATA_RX_CHARACTERISTIC_UUID = "64668730-033f-9393-6ca2-0e9401adeb32"

async def main(address):
    client = BleakClient(address)
    try:
        await client.connect()
        model_number = await client.write_gatt_char(uuid.UUID(DATA_RX_CHARACTERISTIC_UUID), str.encode("5a0507000066"))
        print("Model Number: {0}".format("".join(map(chr, model_number))))
    except Exception as e:
        print(e)
    finally:
        await client.disconnect()

asyncio.run(main(address))