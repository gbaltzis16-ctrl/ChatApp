import os
import websockets
import asyncio

PORT = int(os.environ.get("PORT", 8000))

clients = {} #{ websocket: username }

async def handler(websocket ):
    try:
        username = (await websocket.recv()).strip()

        if not username:
            await websocket.close()
            return

        clients[websocket] = username

        join_Msg=(f"* {username} joined *")
        for client in clients:
            if client != websocket:
                await client.send(join_Msg)

        async for message in websocket:
            message = message.strip()
            if not message:
                continue

            message=f"{username}: {message}"

            for client in clients:
                if client != websocket:
                    await client.send(message)
    finally:
        if websocket in clients:
            username = clients.pop(websocket)
            leave_Msg= f"* {username} left *"
            for client in clients:
                if client != websocket:
                    await client.send(leave_Msg)

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print ("websocket connected on ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())