from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QMenuBar, QAction
from PySide2.QtCore import QThread
import sys
import asyncio
import threading

import config
from section import Section
from ws import WSManager

class WSMThread(QThread):
    def __init__(self, wsm, parent=None):
        super().__init__(parent)
        self.wsm = wsm

    def run(self):
        self.wsm.connect("localhost", 6002, sys.argv[1])

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.sections = [[] for _ in range(len(config.sections))]
        self.connected_callsigns = []
        self.callsign = sys.argv[1]
        self.initUI()
        self.wsm = WSManager(self)
        self.wsm_thread = WSMThread(self.wsm, self)
        self.wsm_thread.start()

    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # create sections
        for i, row in enumerate(config.sections):
            for j, name in enumerate(row):
                self.sections[i].append(Section(name, name==config.inbox, self))
                if name==config.inbox: self.inbox = self.sections[i][j]
                if name != "":
                    if i == 0:
                        self.layout.addWidget(self.sections[i][j], i, j, config.column_spans[j], 1)
                    elif i == 1:
                        self.layout.addWidget(self.sections[i][j], config.column_spans[j], j, 10-config.column_spans[j], 1)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DCS-ElectronicFlightStrips")

        self.initUI()

    def initUI(self):
        self.mainWidget = MainWidget()
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

