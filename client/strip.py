from PySide2.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QPlainTextEdit, QMenu
from PySide2.QtCore import Qt, QSize, QMimeData, QEvent
from PySide2.QtGui import QDrag
import json

from information import *
from stripmenu import StripMenu
import config
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
                 dep: str,
                 arr: str,
                 hdg: str, alt: str, spd: str) -> None:
        super().__init__()
        self.section = section
        self.callsign = callsign
        self.flight_rules = flight_rules
        self.m1 = m1
        self.m3 = m3
        self.service = service
        self.type = type
        self.dep = dep
        self.arr = arr
        self.hdg = hdg
        self.alt = alt
        self.spd = spd
        self.category = category

        data = utils.load_data()
        
        if config.recat:
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
        if config.useEmer:
            if self.m3 in config.emer_squawks:
                self.setStyleSheet(f"background: {config.emer_color}")
            else:
                self.setStyleSheet(f"background: {config.categories[self.category]}")
        else:
            self.setStyleSheet(f"background: {config.categories[self.category]}")

        self.cs_label.render(self.callsign)
        self.dataLabel.render(self.m1, self.m3, self.type, self.wk, self.apc)
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
                "type": "SEND",
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
                    "dep": self.dep,
                    "arr": self.arr,
                    "hdg": self.hdg,
                    "alt": self.alt,
                    "spd": self.spd
                    }
                }
        if self.section.mainWidget.wsm.ws:
            if delete:
                self.section.removeStrip(self, delete=True)
            self.section.mainWidget.wsm.ws.send(json.dumps(data))
