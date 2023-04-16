import asyncio
from websockets.sync.client import connect
import time
import json
import sys

import config

async def main():
    with connect(f"ws://localhost:{config.port}") as sock:
        init = {
                "type": "INIT",
                "callsign": sys.argv[1]
                }
        sock.send(json.dumps(init))
        res = json.loads(sock.recv())
        
        if res["type"] != "SUCCESS":
            exit()
        
        send = {
                "type": "SEND",
                "recipient": "TWR",
                "sender": sys.argv[1],
                "strip": {
                    "callsign": "Toxin 1-1",
                    "flight_rules": "VFR",
                    "service": "N",
                    "m1": "11",
                    "m3": "2000",
                    "category": "Departing",
                    "type": "F18",
                    "dep": "PGUA",
                    "arr": "PGUA",
                    "hdg": "HXXX",
                    "alt": "A050",
                    "spd": "SXXX"
                    }
                }

        sock.send(json.dumps(send))

        while True:
            try:
                message = sock.recv()
                print(f"Received: {message}")
            except KeyboardInterrupt:
                break

asyncio.run(main())

