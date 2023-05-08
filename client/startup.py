from PySide6.QtWidgets import QMainWindow, QGridLayout, QWidget, QMenuBar
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QAction
import sys

import utils
from section import Section
from ws import WSManager

class WSMThread(QThread):
    def __init__(self, wsm, parent=None):
        super().__init__(parent)
        self.wsm = wsm

    def run(self):
        if len(sys.argv) == 2:
            try:
                self.wsm.connect("localhost", 6002, sys.argv[1])
            except:
                print("could not connect to server")
                return
        else:
            return

class MainWidget(QWidget):
    signal = Signal(dict)
    def __init__(self, profile):
        super().__init__()

        self.config = utils.load_config(profile)
        self.sections = [[] for _ in range(len(self.config["sections"]))]
        self.connected_callsigns = []
        if len(sys.argv) == 2:
            self.callsign = sys.argv[1]
        else:
            self.callsign = ""
        self.initUI()
        self.wsm = WSManager(self)
        self.wsm_thread = WSMThread(self.wsm, self)
        self.wsm_thread.start()

        self.signal.connect(self.update_strip)

    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # create sections
        for i, row in enumerate(self.config["sections"]):
            for j, name in enumerate(row):
                self.sections[i].append(Section(name, name==self.config["inbox"], self))
                if name==self.config["inbox"]: self.inbox = self.sections[i][j]
                if name != "":
                    if i == 0:
                        self.layout.addWidget(self.sections[i][j], i, j, self.config["column_spans"][j], 1)
                    elif i == 1:
                        self.layout.addWidget(self.sections[i][j], self.config["column_spans"][j], j, 10-self.config["column_spans"][j], 1)

    def update_strip(self, strip):
        for r in self.sections:
            for section in r:
                for s in section.strips:
                    if s.id == strip["id"]:
                        s.callsign = strip["callsign"]
                        s.flight_rules = strip["flight_rules"]
                        s.m1 = strip["m1"]
                        s.m3 = strip["m3"]
                        s.service = strip["service"]
                        s.type = strip["type"]
                        s.flight = strip["flight"]
                        s.dep = strip["dep"]
                        s.arr = strip["arr"]
                        s.hdg = strip["hdg"]
                        s.alt = strip["alt"]
                        s.spd = strip["spd"]
                        s.category = strip["category"]
                        s.flightplan = strip["flightplan"]

class Window(QMainWindow):
    def __init__(self, profile):
        super().__init__()
        self.setWindowTitle("DCS-ElectronicFlightStrips")
        self.profile = profile

        self.initUI()

    def initUI(self):
        self.mainWidget = MainWidget(self.profile)
        self.setCentralWidget(self.mainWidget)

        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)

        addact = QAction("&Add", self)
        addact.triggered.connect(self.addToInbox)
        self.menubar.addAction(addact)

    def closeEvent(self, e):
        print("exiting")
        e.accept()

    def addToInbox(self):
        for r in self.mainWidget.sections:
            for s in r:
                if s.isInbox:
                    s.addStrip()