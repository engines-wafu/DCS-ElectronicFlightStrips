from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QGridLayout, QPushButton, QDialogButtonBox, QVBoxLayout

class StripMenu(QDialog):
    def __init__(self, strip):
        super().__init__()
        self.setWindowTitle("Strip Options")
        self.strip = strip

        self.initUI()

    def initUI(self):
        self.btns = QDialogButtonBox(QDialogButtonBox.Ok)
        self.btns.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.btns)
