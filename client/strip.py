from PySide6.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QPlainTextEdit, QMenu
from PySide6.QtCore import Qt, QSize, QMimeData, QEvent
from PySide6.QtGui import QDrag
import json

from information import *
from stripmenu import StripMenu
import utils

class Strip(QFrame):
    def __init__(self,
                 section,
                 callsign: str,
                 flight_rules: str,
                 service: str,
                 m1: str,
                 m3: str,
                 category: str,
                 type: str,
                 size: int,
                 dep: str,
                 arr: str,
                 hdg: str, alt: str, spd: str,
                 flightplan: dict) -> None:
        super().__init__()
        self.section = section
        self.callsign = callsign
        self.flight_rules = flight_rules
        self.m1 = m1
        self.m3 = m3
        self.service = service
        self.type = type
        self.flight = size
        self.dep = dep
        self.arr = arr
        self.hdg = hdg
        self.alt = alt
        self.spd = spd
        self.category = category
        self.flightplan = flightplan
        self.config = self.section.config

        data = utils.load_data()
        
        if self.config["use_recat"]:
            self.wk = data[self.type]["RECAT"]
        else:
            self.wk = data[self.type]["WTC"]

        self.apc = data[self.type]["APC"]

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(1)

        self.initUI()

    def initUI(self) -> None:
        self.cs_label = CsLabel(self)
        self.cs_label.move(0, 0)

        self.dataLabel = Data(self)
        self.dataLabel.move(60, 0)

        self.ruleLabel = Rule(self)
        self.ruleLabel.move(150, 0)

        self.serviceLabel = Service(self)
        self.serviceLabel.move(180, 0)

        self.navLabel = Nav(self)
        self.navLabel.move(210, 0)

        self.comment = Comment(self)
        self.comment.move(340, 0)

        self.render()

    def render(self) -> None:
        if self.config["use_emer"]:
            if self.m3 in self.config["emer_squawks"]:
                c = self.config["emer_color"]
                self.setStyleSheet(f"background: {c}")
            else:
                c = self.config["categories"][self.category]
                self.setStyleSheet(f"background: {c}")
        else:
            c = self.config["categories"][self.category]
            self.setStyleSheet(f"background: {c}")

        self.cs_label.render(self.callsign)
        self.dataLabel.render(self.m1, self.m3, self.type, self.flight, self.wk, self.apc)
        self.ruleLabel.render(self.flight_rules)
        self.serviceLabel.render(self.service)
        self.navLabel.render(self.dep, self.arr, self.hdg, self.alt, self.spd)

    def sizeHint(self) -> QSize:
        return QSize(100, 50)

    def mouseMoveEvent(self, e: QEvent) -> None:
        if e.buttons() == Qt.LeftButton:
            self.section.removeStrip(self)
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            drag.exec_(Qt.MoveAction)

    def mouseDoubleClickEvent(self, e: QEvent) -> None:
        menu = StripMenu(self, self.section)
        menu.exec()

    def contextMenuEvent(self, e: QEvent) -> None:
        menu = QMenu(self)
        delAct = menu.addAction("Delete")
        sendMenu = menu.addMenu("Send To")
        duplMenu = menu.addMenu("Duplicate To")
        sendActions = []
        duplActions = []
        for callsign in self.section.mainWidget.connected_callsigns:
            sendActions.append(sendMenu.addAction(callsign))
            duplActions.append(duplMenu.addAction(callsign))

        action = menu.exec_(self.mapToGlobal(e.pos()))

        if action == delAct:
            self.section.removeStrip(self, delete=True)
        elif action in sendActions:
            ind = sendActions.index(action)
            self.send(self.section.mainWidget.connected_callsigns[ind])
        elif action in duplActions:
            ind = duplActions.index(action)
            self.send(self.section.mainWidget.connected_callsigns[ind], delete=False)

    def send(self, recipient, delete=True):
        data = {
                "type": "SEND" if delete else "DUPLICATE",
                "recipient": recipient,
                "sender": self.section.mainWidget.callsign,
                "strip": {
                    "callsign": self.callsign,
                    "flight_rules": self.flight_rules,
                    "service": self.service,
                    "m1": self.m1,
                    "m3": self.m3,
                    "category": self.category,
                    "type": self.type,
                    "flight": self.flight,
                    "dep": self.dep,
                    "arr": self.arr,
                    "hdg": self.hdg,
                    "alt": self.alt,
                    "spd": self.spd,
                    "flight_plan": self.flightplan
                    }
                }
        if self.section.mainWidget.wsm.ws:
            if delete:
                self.section.removeStrip(self, delete=True)
            self.section.mainWidget.wsm.ws.send(json.dumps(data))
