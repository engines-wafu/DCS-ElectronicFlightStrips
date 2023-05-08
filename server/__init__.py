import asyncio
import websockets
from websockets import WebSocketServerProtocol
import json
import random

import config

"""
STRIP KEYS:
id: random number 0-10_000
callsign
flight_rules
service
m1
m3
category
type
flight
dep
arr
hdg
alt
spd
flight plan:
    route
    equipment
    altitude
controllers
"""

class Server:
    clients = set()
    controllers = {}
    strips = {}

    def find_strip(self, strip: dict) -> int:
        try:
            return self.strips.index(strip)
        except:
            return -1

    def find_cs(self, ws: WebSocketServerProtocol) -> str:
        for k, v in self.controllers.items():
            if v == ws:
                return k
            
        return ""

    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        print(f"{ws.remote_address} Connected")

    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        if not ws in self.clients:
            return

        cs = ""
        for callsign in list(self.controllers.keys()):
            if self.controllers[callsign]["ws"] == ws:
                cs = callsign
                self.controllers.pop(callsign, None)

        self.clients.remove(ws)
        print(f"{ws.remote_address} Disconnected")
        await self.send_to_all(json.dumps({"type": "DISCONNECT", "callsign": cs}))
        print(self.controllers.keys())

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
            if data["callsign"] in list(self.controllers.keys()):
                res = {
                        "type": "ERROR",
                        "message": "Callsign already connected"
                        }
                await ws.send(json.dumps(res))
            else:
                res = {
                        "type": "SUCCESS",
                        "message": "connection successful",
                        "callsigns": list(self.controllers.keys())
                        }
                await ws.send(json.dumps(res))
                notify = {
                        "type": "CONNECT",
                        "callsign": data["callsign"]
                        }
                await self.send_to_all(json.dumps(notify), exclude=[ws])
                self.controllers[data["callsign"]] = {"ws": ws}
                print(list(self.controllers.keys()))

        if data["type"] == "SEND" or data["type"] == "DUPLICATE":
            if data["recipient"] not in list(self.controllers.keys()):
                res = {
                        "type": "ERROR",
                        "message": "Callsign does not exist"
                        }
                await ws.send(json.dumps(res))
            else:
                recipient = self.controllers[data["recipient"]]["ws"]
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

        if data["type"] == "REQUEST_SQUAWK":
            unavailable_squawks = set()
            for strip in self.strips:
                unavailable_squawks.add(strip["m3"])

            res = {
                "type": "SQUAWKS",
                "squawks": unavailable_squawks
            }

        if data["type"] == "STRIP":
            strip = data["strip"]
            if strip in self.strips:
                ind = strip["id"]
                for k, v in strip.items():
                    self.strips[ind][k] = v

                c = self.find_cs(ws)
                if not c in self.strips[ind]["controllers"]:
                    self.strips[ind]["controllers"].append(c)

            else:
                strip["controllers"] = [self.find_cs(ws)]

                self.strips[strip["id"]] = strip




if __name__ == "__main__":
    server = Server()
    start_server = websockets.serve(server.ws_handler, "0.0.0.0", config.port)
    print("Server Started")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()
