import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("PyQt6 Test")
window.setGeometry(800, 800, 300, 200)

label = QLabel("Hello PyQt6!", parent=window)
label.move(100, 80)

window.show()
sys.exit(app.exec())
