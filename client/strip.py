from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QPlainTextEdit, QMenu
from PyQt5.QtCore import Qt, QSize, QMimeData
from PyQt5.QtGui import QDrag

from information import *
from stripmenu import StripMenu
import config

class Strip(QFrame):
    def __init__(self,
                 section,
                 callsign,
                 flight_rules,
                 service,
                 m1,
                 m3,
                 category,
                 type,
                 dep,
                 arr,
                 hdg, alt, spd):
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
        self.wk = "M"
        self.apc = "A"

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(1)

        self.initUI()

    def initUI(self):
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

    def render(self):
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
        menu = StripMenu(self, self.section)
        menu.exec()

    def contextMenuEvent(self, e):
        menu = QMenu(self)
        delAct = menu.addAction("Delete")
        action = menu.exec_(self.mapToGlobal(e.pos()))

        if action == delAct:
            self.section.removeStrip(self)
