from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QMenuBar
import sys

import config
from section import Section

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.sections = [[] for _ in range(len(config.sections))]
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # create sections
        for i, row in enumerate(config.sections):
            for j, name in enumerate(row):
                self.sections[i].append(Section(name, name==config.inbox))
                if name != "":
                    if i == 0:
                        self.layout.addWidget(self.sections[i][j], i, j, config.column_spans[j], 1)
                    elif i == 1:
                        self.layout.addWidget(self.sections[i][j], config.column_spans[j], j, 10-config.column_spans[j], 1)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DCS-ElectronicFlightStrips")

        self.initUI()

    def initUI(self):
        self.mainWidget = MainWidget()
        self.setCentralWidget(self.mainWidget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

