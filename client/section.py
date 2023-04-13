from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QPushButton, QScrollArea, QWidget

from strip import Strip
from stripmenu import StripMenu
import utils
import config
from random import randint

class Section(QGroupBox):
    def __init__(self, name, isInbox, mainWidget):
        super().__init__(name)
        self.strips = []
        self.name = name
        self.isInbox = isInbox
        self.mainWidget = mainWidget

        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        if self.isInbox:
            self.addButton = QPushButton("Add")
            self.addButton.clicked.connect(self.addStrip)

            layout.addWidget(self.addButton)

        scroll = QScrollArea(self)
        layout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)

        self.scrollLayout = QVBoxLayout(scrollContent)
        self.scrollLayout.setAlignment(Qt.AlignTop)
        scrollContent.setLayout(self.scrollLayout)
        scroll.setWidget(scrollContent)

    def addStrip(self):
        strip = Strip(self,
                      config.defaults["callsign"],
                      config.defaults["flight rules"],
                      config.defaults["service"],
                      config.defaults["m1"],
                      utils.generate_squawk(config.defaults["service"], config.defaults["flight rules"], self.mainWidget),
                      config.defaults["category"],
                      config.defaults["type"],
                      config.defaults["fields"],
                      config.defaults["fields"],
                      config.defaults["hdg"],
                      config.defaults["alt"],
                      config.defaults["spd"]
                      )

        stripmenu = StripMenu(strip, self)
        stripmenu.exec()
        self.strips.append(strip)
        self.scrollLayout.addWidget(strip)

    def removeStrip(self, strip):
        try:
            self.strips.remove(strip)
            self.scrollLayout.removeWidget(strip)
        except:
            return

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        pos = e.pos()
        strip = e.source()
        if strip in self.strips:
            return

        inserted = False
        
        for n in range(len(self.strips)):
            w = self.strips[n]
            if pos.y() < w.y():
                self.strips.insert(n-1, strip)
                self.scrollLayout.insertWidget(n-1, strip)
                inserted = True
                break

        if not inserted:
            self.strips.append(strip)
            self.scrollLayout.addWidget(strip)

        strip.section = self

        e.accept()
