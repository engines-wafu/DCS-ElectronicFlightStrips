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
        self.clients.remove(ws)
        print(f"{ws.remote_address} Disconnected")

    async def send_to_clients(self, message: str) -> None:
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def ws_handler(self, ws: WebSocketServerProtocol, uri: str) -> None:
        await self.register(ws)
        try:
            async for message in ws:
                await self.on_message(ws, message)
        finally:
            await self.unregister(ws)

    async def on_message(self, ws: WebSocketServerProtocol, message: str) -> None:
        data = json.loads(message)
        if data["type"] == "INIT":
            if data["callsign"] in list(self.callsigns.keys()):
                res = {
                        "type": "ERROR",
                        "message": "Callsign already connected"
                        }
                await ws.send(json.dumps(res))
            else:
                self.callsigns[data["callsign"]] = {"ws": ws}
                res = {
                        "type": "SUCCESS",
                        "message": "connection successful"
                        }
                await ws.send(json.dumps(res))
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

                res = {
                        "type": "SUCCESS",
                        "message": "Sent Strip"
                        }

                await ws.send(json.dumps(res))



if __name__ == "__main__":
    server = Server()
    start_server = websockets.serve(server.ws_handler, "localhost", config.port)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()
