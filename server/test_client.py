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
                "strip": {"callsign": "Toxin 1-1"}
                }

        sock.send(json.dumps(send))

        while True:
            try:
                message = sock.recv()
                print(f"Received: {message}")
            except KeyboardInterrupt:
                break

asyncio.run(main())

