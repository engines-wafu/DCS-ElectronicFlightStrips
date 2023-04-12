from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QPlainTextEdit, QMenu
from PyQt5.QtCore import Qt, QSize, QMimeData
from PyQt5.QtGui import QDrag

from information import *

class Strip(QFrame):
    def __init__(self, section, callsign, flight_rules, squawk):
        super().__init__()
        self.section = section
        self.callsign = callsign
        self.flight_rules = flight_rules
        self.squawk = squawk

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(1)

        self.initUI()

    def initUI(self):
        self.setStyleSheet("background: lightblue")

        self.cs_label = CsLabel(self, self.callsign)
        self.cs_label.move(0, 0)

        self.data = Data(self, "11", self.squawk, "A32N", "UM")
        self.data.move(60, 0)

        self.rule = Rule(self, self.flight_rules)
        self.rule.move(150, 0)

        self.service = Service(self, "TS")
        self.service.move(180, 0)

        self.nav = Nav(self, "PGUA", "PGUA")
        self.nav.move(210, 0)

        self.comment = Comment(self)
        self.comment.move(340, 0)

    def sizeHint(self):
        return QSize(100, 50)

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            self.section.removeStrip(self)
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            drag.exec_(Qt.MoveAction)

    def mouseDoubleClickEvent(self, e):
        print(f"{self.squawk} options")

    def contextMenuEvent(self, e):
        menu = QMenu(self)
        delAct = menu.addAction("Delete")
        action = menu.exec_(self.mapToGlobal(e.pos()))

        if action == delAct:
            self.section.removeStrip(self)
