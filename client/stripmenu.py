from PySide2 import QtWidgets
from PySide2.QtWidgets import QDialog, QFormLayout, QGridLayout, QPushButton, QDialogButtonBox, QLabel, QLineEdit, QComboBox, QSpacerItem, QSizePolicy, QWidget, QMessageBox, QHBoxLayout

import config
import utils

class StripMenu(QDialog):
    def __init__(self, strip, section) -> None:
        super().__init__()
        self.setWindowTitle("Strip Options")
        self.strip = strip
        self.section = section

        self.data = utils.load_data()
        self.aerodromes = utils.load_aerodromes()

        self.initUI()

    def initUI(self) -> None:
        self.btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.btns.accepted.connect(self.submit)
        self.btns.rejected.connect(self.reject)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.data1 = QFormLayout()
        self.data2 = QFormLayout()

        self.flight1 = QFormLayout()
        self.flight2 = QFormLayout()

        self.cs_box = QLineEdit()
        self.cs_box.setText(self.strip.callsign)
        self.data1.addRow("Callsign:", self.cs_box)

        self.m3_box = M3Box(self)
        self.m3_box.setText(self.strip.m3)
        self.data2.addRow("Mode 3:", self.m3_box)

        self.m1_box = QLineEdit()
        self.m1_box.setText(self.strip.m1)
        self.data2.addRow("Mode 1:", self.m1_box)

        self.cat_box = QComboBox()
        self.cat_box.addItems(list(config.categories.keys()))
        self.cat_box.setCurrentText(self.strip.category)
        self.data1.addRow("Category:", self.cat_box)

        self.rules_box = QComboBox()
        self.rules_box.addItems(list(config.flight_rules))
        self.rules_box.setCurrentText(self.strip.flight_rules)
        self.data1.addRow("Flight Rules:", self.rules_box)
       
        self.service_box = QComboBox()
        self.service_box.addItems(list(config.services))
        self.service_box.setCurrentText(self.strip.service)
        self.data2.addRow("Service:", self.service_box)

        self.type_box = QLineEdit()
        self.type_box.setText(self.strip.type)
        self.data1.addRow("Type:", self.type_box)

        self.flight1.addRow(" ", QWidget())
        self.flight2.addRow(" ", QWidget())

        self.dep_box = QLineEdit()
        self.dep_box.setText(self.strip.dep)
        self.flight1.addRow("Departure:  ", self.dep_box)

        self.arr_box = QLineEdit()
        self.arr_box.setText(self.strip.arr)
        self.flight2.addRow("Arrival:", self.arr_box)

        self.layout.addLayout(self.data1, 0, 0)
        self.layout.addLayout(self.data2, 0, 1)

        self.layout.addLayout(self.flight1, 1, 0)
        self.layout.addLayout(self.flight2, 1, 1)

        self.layout.addWidget(self.btns, 2, 1)

    def submit(self) -> None:
        if not utils.validate_squawk(self.m3_box.text().strip()):
            print("Invalid squawk")
            self.dialog("Invalid M3 Squawk")
            return
        if not utils.validate_squawk(self.m1_box.text().strip()):
            print("Invalid M1")
            self.dialog("Invalid M1 Squawk")
            return
        if not self.type_box.text().strip() in list(self.data.keys()):
            print("Invalid type")
            self.dialog("Invalid type")
            return
        if not self.arr_box.text().strip() in list(self.aerodromes.keys()):
            print("Invalid arrival")
            self.dialog("Invalid Arrival")
            return
        if not self.dep_box.text().strip() in list(self.aerodromes.keys()):
            print("Invalid departure")
            self.dialog("Invalid Departure")
            return

        self.strip.callsign = self.cs_box.text()
        self.strip.m3 = self.m3_box.text()
        self.strip.category = self.cat_box.currentText()
        self.strip.flight_rules = self.rules_box.currentText()
        self.strip.service = self.service_box.currentText()
        self.strip.type = self.type_box.text().strip()

        if config.recat:
            self.strip.wk = self.data[self.strip.type]["RECAT"]
        else:
            self.strip.wk = self.data[self.strip.type]["WTC"]

        self.strip.apc = self.data[self.strip.type]["APC"]

        self.strip.dep = self.dep_box.text()
        self.strip.arr = self.arr_box.text()

        self.strip.render()
        self.accept()

    def reject(self) -> None:
        self.accept()

    def dialog(self, msg: str) -> None:
        dlg = QMessageBox(self)
        dlg.setText(msg)
        dlg.setWindowTitle(msg)

        dlg.exec()


class M3Box(QWidget):
    def __init__(self, menu: StripMenu) -> None:
        super().__init__()
        self.menu = menu
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.box = QLineEdit()
        self.gen = QPushButton("Gen")
        self.gen.clicked.connect(self.genClicked)

        self.layout.addWidget(self.box)
        self.layout.addWidget(self.gen)
        self.setLayout(self.layout)

    def text(self) -> str:
        return self.box.text()

    def setText(self, txt: str) -> None:
        self.box.setText(txt)

    def genClicked(self) -> None:
        m = utils.generate_squawk(self.menu.service_box.currentText(), self.menu.rules_box.currentText(), self.menu.section.mainWidget)
        self.box.setText(m)
