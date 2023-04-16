import websockets
from websockets.sync.client import connect
import threading
import json
import sys

from strip import Strip
import config

class WSManager:
    def __init__(self, mainWidget):
        self.mainWidget = mainWidget
        self.ws = None
        self.callsign = None

    def connect(self, host, port, callsign):
        with connect(f"ws://{host}:{port}") as ws:
            self.ws = ws

            init = {"type": "INIT",
                    "callsign": callsign}
            self.callsign = callsign

            self.send(json.dumps(init))

            res = json.loads(ws.recv())
            print(f"Received: {res}")
            if res["type"] != "SUCCESS":
                print("ERRROR", res["message"])

            self.mainWidget.connected_callsigns = res["callsigns"]

            while True:
                try:
                    message = ws.recv()
                    self.on_message(message)
                except KeyboardInterrupt:
                    print("received keyboard interrupt")
                    break

        self.ws = None

    def on_message(self, message):
        print(f"Received: {message}")
        data = json.loads(message)
        
        if data["type"] == "CONNECT":
           self.mainWidget.connected_callsigns.append(data["callsign"])
        if data["type"] == "DISCONNECT":
            self.mainWidget.connected_callsigns.remove(data["callsign"])

        if data["type"] == "SEND":
            self.mainWidget.inbox.signal.emit(data["strip"]) 

        print(self.mainWidget.connected_callsigns)

    def send(self, message):
        self.ws.send(message)
        print(f"Sent: {message}")

if __name__ == "__main__":
    wsm = WSManager(None)
    wsm.connect("localhost", 6002, "GND")
    message = {"type": "PING"}
    wsm.send(json.dumps(message))
    wsm.listen()
    wsm.send(json.dumps({"type": "PING"}))
