import os
import websockets
import asyncio

PORT = int(os.environ.get("PORT", 8000))

clients = {} #{ websocket: username }

async def handler(ws):
    try:
        username = (await ws.recv()).strip()

        if not username:
            await ws.close()
            return

        clients[ws] = username

        join_Msg=(f"* {username} joined *")
        for client in clients:
            if client != ws:
                await client.send(join_Msg)

        async for message in ws:
            message = message.strip()
            if not message:
                continue

            message=f"{username}: {message}"

            for client in clients:
                if client != ws:
                    await client.send(message)
    finally:
        if ws in clients:
            username = clients.pop(ws)
            leave_Msg= f"* {username} left *"
            for client in clients:
                if client != ws:
                    await client.send(leave_Msg)

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print ("websocket connected on ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())