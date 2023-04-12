from PyQt5.QtWidgets import QLabel, QSizePolicy, QPlainTextEdit
from PyQt5.QtCore import Qt, QSize

class CsLabel(QLabel):
    def __init__(self, surf, cs):
        super().__init__(surf)
        self.cs = cs
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setText(cs)
        self.setStyleSheet("margin: 5px; border-right: 1px solid black")
        self.setAlignment(Qt.AlignCenter)

    def sizeHint(self):
        return QSize(70, 50)

class Data(QLabel):
    def __init__(self, surf, m1, m3, acft, wk):
        super().__init__(surf)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setText(f"({m1}) {m3}\n{wk}|{acft}")
        self.setStyleSheet("margin: 5px; border-right: 1px solid black")
        self.setAlignment(Qt.AlignCenter)

    def sizeHint(self):
        return QSize(100, 50)

class Rule(QLabel):
    def __init__(self, surf, rule):
        super().__init__(surf)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setText(rule[0].upper())
        self.setStyleSheet("margin: 5px; border-right: 1px solid black; font-size: 20px")
        self.setAlignment(Qt.AlignCenter)

    def sizeHint(self):
        return QSize(40, 50)

class Service(QLabel):
    def __init__(self, surf, service):
        super().__init__(surf)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setText(service)
        self.setStyleSheet("margin: 5px; border-right: 1px solid black; font-size: 17px")
        self.setAlignment(Qt.AlignCenter)

    def sizeHint(self):
        return QSize(40, 50)

class Nav(QLabel):
    def __init__(self, surf, dep, arr):
        super().__init__(surf)
        self.dep = dep
        self.arr = arr
        self.hdg = "H060"
        self.alt = "A130"
        self.spd = "SXXX"

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setText(f"{self.dep}|{self.arr}\n{self.hdg}|{self.alt}|{self.spd}")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("margin: 5px; border-right: 1px solid black")

    def sizeHint(self):
        return QSize(130, 50)

class Comment(QPlainTextEdit):
    def __init__(self, surf):
        super().__init__(surf)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet("margin: 5px;")

    def sizeHint(self):
        return QSize(220, 50)

