import os

import websockets
import websockets as ws
import asyncio

PORT = int(os.environ.get("PORT", 8000))

clients = set()

async def handler(websocket ):
    clients.add(websocket)
    try:
        async for message in websocket:
            for client in clients:
                if client != websocket:
                    await client.send(message)
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print ("websocket connected on ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())