import asyncio
import websockets
from websockets import WebSocketServerProtocol
import websockets
import json

import config

class Server:
    clients = set()
    callsigns = {}

    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        print(f"{ws.remote_address} Connected")

    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        if not ws in self.clients:
            return

        cs = ""
        for callsign in list(self.callsigns.keys()):
            if self.callsigns[callsign]["ws"] == ws:
                cs = callsign
                self.callsigns.pop(callsign, None)

        self.clients.remove(ws)
        print(f"{ws.remote_address} Disconnected")
        await self.send_to_all(json.dumps({"type": "DISCONNECT", "callsign": cs}))
        print(self.callsigns.keys())

    async def send_to_all(self, message: str, exclude: list=[]) -> None:
        if self.clients:
            for client in self.clients:
                if not client in exclude:
                    await client.send(message)

        print(f"Sent to all: {message}")

    async def ws_handler(self, ws: WebSocketServerProtocol, uri: str) -> None:
        await self.register(ws)
        try:
            async for message in ws:
                await self.on_message(ws, message)
        except:
            await self.unregister(ws)
        finally:
            await self.unregister(ws)

    async def on_message(self, ws: WebSocketServerProtocol, message: str) -> None:
        print(f"Received: {message}")
        data = json.loads(message)
        if data["type"] == "PING":
            await ws.send(json.dumps({"type": "PONG"}))

        if data["type"] == "INIT":
            if data["callsign"] in list(self.callsigns.keys()):
                res = {
                        "type": "ERROR",
                        "message": "Callsign already connected"
                        }
                await ws.send(json.dumps(res))
            else:
                res = {
                        "type": "SUCCESS",
                        "message": "connection successful",
                        "callsigns": list(self.callsigns.keys())
                        }
                await ws.send(json.dumps(res))
                notify = {
                        "type": "CONNECT",
                        "callsign": data["callsign"]
                        }
                await self.send_to_all(json.dumps(notify), exclude=[ws])
                self.callsigns[data["callsign"]] = {"ws": ws}
                print(list(self.callsigns.keys()))

        if data["type"] == "SEND":
            if data["recipient"] not in list(self.callsigns.keys()):
                res = {
                        "type": "ERROR",
                        "message": "Callsign does not exist"
                        }
                await ws.send(json.dumps(res))
            else:
                recipient = self.callsigns[data["recipient"]]["ws"]
                send = {
                        "type": "SEND",
                        "sender": data["sender"],
                        "strip": data["strip"]
                        }
                await recipient.send(json.dumps(send))
                print(f"Sent: {send}")

                res = {
                        "type": "SUCCESS",
                        "message": "Sent Strip"
                        }

                await ws.send(json.dumps(res))



if __name__ == "__main__":
    server = Server()
    start_server = websockets.serve(server.ws_handler, "localhost", config.port)
    print("Server Started")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()
