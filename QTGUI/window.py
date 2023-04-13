import sys
import GUIClass
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

app = QApplication(sys.argv)
window = GUIClass.GUI()

window.show()
sys.exit(app.exec_())
