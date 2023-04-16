from PySide2.QtCore import Qt, QEvent, Signal, QObject
from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QPushButton, QScrollArea, QWidget

from strip import Strip
from stripmenu import StripMenu
import utils
from random import randint

class Section(QGroupBox):
    signal = Signal(dict)
    def __init__(self, name: str, isInbox: bool, mainWidget) -> None:
        super().__init__(name)
        self.config = mainWidget.config
        self.strips = []
        self.signal.connect(self.receiveStrip)
        self.name = name
        self.isInbox = isInbox
        self.mainWidget = mainWidget

        self.initUI()

    def initUI(self) -> None:
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

    def receiveStrip(self, data: dict) -> None:
        rule = data["flight_rules"] if data["flight_rules"] in list(self.config["flight_rules"].keys()) else self.config["defaults"]["flight rules"]
        service = data["service"] if data["service"] in list(self.config["services"].keys()) else self.config["defaults"]["service"]
        category = data["category"] if data["category"] in list(self.config["categories"].keys()) else self.config["defaults"]["category"]

        strip = Strip(self,
                      data["callsign"],
                      rule,
                      service,
                      data["m1"],
                      data["m3"],
                      category,
                      data["type"],
                      data["dep"],
                      data["arr"],
                      data["hdg"],
                      data["alt"],
                      data["spd"]
                      )

        self.strips.append(strip)
        self.scrollLayout.addWidget(strip)

    def addStrip(self) -> None:
        strip = Strip(self,
                      self.config["strip_defaults"]["callsign"],
                      self.config["strip_defaults"]["flight_rules"],
                      self.config["strip_defaults"]["service"],
                      self.config["strip_defaults"]["m1"],
                      utils.generate_squawk(self.config["strip_defaults"]["service"], self.config["strip_defaults"]["flight_rules"], self.mainWidget),
                      self.config["strip_defaults"]["category"],
                      self.config["strip_defaults"]["type"],
                      self.config["strip_defaults"]["flight_size"],
                      self.config["strip_defaults"]["departure_field"],
                      self.config["strip_defaults"]["arrival_field"],
                      self.config["strip_defaults"]["hdg"],
                      self.config["strip_defaults"]["alt"],
                      self.config["strip_defaults"]["spd"]
                      )

        stripmenu = StripMenu(strip, self)
        stripmenu.exec()

        self.strips.append(strip)
        self.scrollLayout.addWidget(strip)

    def removeStrip(self, strip: Strip, delete: bool=False):
        self.strips.remove(strip)
        self.scrollLayout.removeWidget(strip)
        self.scrollLayout.activate()
        if delete:
            strip.setParent(None)
            strip.deleteLater()

    def dragEnterEvent(self, e: QEvent) -> None:
        e.accept()

    def dropEvent(self, e: QEvent) -> None:
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
