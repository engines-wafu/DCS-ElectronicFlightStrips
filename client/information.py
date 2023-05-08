from PySide6.QtWidgets import QLabel, QSizePolicy, QPlainTextEdit, QFrame, QComboBox, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter

class CsLabel(QLabel):
    def __init__(self, surf):
        super().__init__(surf)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setStyleSheet("margin: 5px; border-right: 1px solid black")
        self.setAlignment(Qt.AlignCenter)

    def render(self, cs):
        self.cs = cs
        self.setText(cs)

    def sizeHint(self):
        return QSize(70, 50)

class Data(QFrame):
    def __init__(self, surf):
        super().__init__(surf)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setObjectName("data")
        self.setStyleSheet("#data {margin: 5px; border-right: 1px solid black}")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.label1 = QLabel()
        self.label1.setAlignment(Qt.AlignCenter)
        self.label2 = QLabel()
        self.label2.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.label2)

    def render(self, m1: str, m3: str, acft: str, num: int, wk: str, apc: str):
        self.label1.setText(f"({m1}) {m3}")
        self.label2.setText(f"{wk}|{num}x {acft}|{apc}")

    def sizeHint(self):
        return QSize(100, 50)

class Rule(QLabel):
    def __init__(self, surf):
        super().__init__(surf)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setStyleSheet("margin: 5px; border-right: 1px solid black; font-size: 20px")
        self.setAlignment(Qt.AlignCenter)

    def render(self, rule):
        self.setText(rule[0].upper())

    def sizeHint(self):
        return QSize(40, 50)

class Service(QLabel):
    def __init__(self, surf):
        super().__init__(surf)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setStyleSheet("margin: 5px; border-right: 1px solid black; font-size: 17px")
        self.setAlignment(Qt.AlignCenter)

    def render(self, service):
        self.setText(service)

    def sizeHint(self):
        return QSize(40, 50)

class Nav(QFrame):
    def __init__(self, strip):
        super().__init__(strip)
        self.strip = strip

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.nLayout = QHBoxLayout()
        self.nLayout.setSpacing(0)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setObjectName("NavFrame")
        self.setStyleSheet("#NavFrame {margin: 5px; border-right: 1px solid black}")
        self.setFrameShape(QFrame.NoFrame)
        self.setLineWidth(0)

        self.label = QLabel(self)
        self.label.setStyleSheet("padding-top: -5px; margin-top: -5px")
        self.label.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.layout.addWidget(self.label)
        
        self.layout.addLayout(self.nLayout)
        self.hdg_box = AltComboBox()
        #self.layout.addWidget(self.hdg_box, 1, 0)
        self.nLayout.addWidget(self.hdg_box)
        self.hdg_box.addItem("HXXX")
        self.hdg_box.addItems([f"H{i:03}" for i in range(5, 365, 5)])
        self.alt_box = AltComboBox()
        #self.layout.addWidget(self.alt_box, 1, 1)
        self.nLayout.addWidget(self.alt_box)
        self.alt_box.addItem("AXXX")
        self.alt_box.addItems([f"A{i:03}" for i in range(0, 405, 5)])
        self.alt_box.addItems([f"A{i:03}" for i in range(410, 610, 10)])
        self.spd_box = AltComboBox()
        #self.layout.addWidget(self.spd_box, 1, 2)
        self.nLayout.addWidget(self.spd_box)
        self.spd_box.addItem("SXXX")
        self.spd_box.addItems([f"S{i:03}" for i in range(0, 310, 10)])

        self.hdg_box.activated.connect(self.onBoxChanged)
        self.alt_box.activated.connect(self.onBoxChanged)
        self.spd_box.activated.connect(self.onBoxChanged)

        self.layout.insertStretch(-1, 1)

    def render(self, dep, arr, hdg, alt, spd):
        self.dep = dep
        self.arr = arr
        self.hdg = hdg
        self.alt = alt
        self.spd = spd
        
        self.label.setText(f"{self.dep} | {self.arr}")
        self.hdg_box.setCurrentText(self.hdg)
        self.alt_box.setCurrentText(self.alt)
        self.spd_box.setCurrentText(self.spd)

    def sizeHint(self):
        return QSize(130, 50)

    def onBoxChanged(self, v):
        self.strip.hdg = self.hdg_box.currentText()
        self.strip.alt = self.alt_box.currentText()
        self.strip.spd = self.spd_box.currentText()

class Comment(QPlainTextEdit):
    def __init__(self, surf):
        super().__init__(surf)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet("margin: 5px;")

    def sizeHint(self):
        return QSize(220, 50)

class AltComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""QComboBox::drop-down {border-width: 0px;} QComboBox::down-arrow {image: url(noimg); border-width: 0px;}
                           QComboBox {combobox-popup: 0;}
                           QComboBox QAbstractItemView {min-width: 150px;}""")
        self.setMaxVisibleItems(10)
        self.setMinimumContentsLength(4)

    def paintEvent(self, e):
        p = QPainter()
        p.begin(self)
        p.drawText(e.rect(), Qt.AlignCenter, self.currentText())
        p.end()

