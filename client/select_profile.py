from PySide6.QtWidgets import QDialog, QComboBox, QVBoxLayout, QDialogButtonBox

import utils
import sys

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