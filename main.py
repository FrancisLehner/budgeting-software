from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

app = QApplication([])

window = QMainWindow()
window.setMinimumSize(800, 600)
window.setWindowTitle('Budget Tracker')


window.show()
app.exec()