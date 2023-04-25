from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QMenuBar, QAction, QDialog, QComboBox, QVBoxLayout, QDialogButtonBox
from PySide2.QtCore import QThread
import sys
import asyncio
import threading

from section import Section
from ws import WSManager
import utils

class WSMThread(QThread):
    def __init__(self, wsm, parent=None):
        super().__init__(parent)
        self.wsm = wsm

    def run(self):
        if len(sys.argv) == 2:
            try:
                self.wsm.connect("localhost", 6002, sys.argv[1])
            except:
                return
        else:
            return

class MainWidget(QWidget):
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

class SelectProfile(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Choose Profile")
        self.profile = None
        self.config = utils.load_config()
        res = utils.validate_config(self.config)
        if not res:
            sys.exit(1)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        profiles = [profile["profile_name"] for profile in self.config]
        self.box = QComboBox()
        self.box.addItems(profiles)

        self.layout.addWidget(self.box)

        self.btns = QDialogButtonBox(QDialogButtonBox.Ok)
        self.btns.accepted.connect(self.submit)

        self.layout.addWidget(self.btns)

    def submit(self):
        self.profile = self.box.currentText()
        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = SelectProfile()
    dlg.exec()

    win = Window(dlg.profile)
    win.show()
    sys.exit(app.exec_())

