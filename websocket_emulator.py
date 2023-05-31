import asyncio
import websockets
import json
import random

async def server(websocket, path):
    while True:
        data = {
            "battery": random.randint(0, 100),
            "checksumByte": random.randint(0, 255),
            "commandByte": random.randint(0, 255),
            "cureState": random.randint(0, 100),
            "cureTimeMinute": random.randint(0, 59),
            "cureTimeSecound": random.randint(0, 59),
            "electricOverLoad": random.choice([True, False]),
            "intensity": random.randint(0, 10),
            "intensityLock": random.choice([True, False]),
            "lengthByte": random.randint(0, 255),
            "mode": random.randint(0, 10),
            "program": random.randint(0, 10),
            "startByte": random.randint(0, 255),
        }
        await websocket.send(json.dumps(data))
        await asyncio.sleep(3)  # wait for 3 seconds before next send

start_server = websockets.serve(server, 'localhost', 8765)

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()