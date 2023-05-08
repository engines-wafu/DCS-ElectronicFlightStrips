from PySide6.QtWidgets import QApplication
from select_profile import SelectProfile
from startup import Window
import sys

if __name__ == "__main__":
	app = QApplication(sys.argv)
	dlg = SelectProfile()
	dlg.exec()

	win = Window(dlg.profile)
	win.show()
	sys.exit(app.exec())

