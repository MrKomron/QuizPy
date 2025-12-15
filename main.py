# main.py
# Dit is het startpunt van het programma.

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton

from auth import AuthWindow

import sys


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    # Opzetten van de pagina.
    def init_ui(self):
        self.setWindowTitle("QuizPy")
        self.resize(780, 915)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.addStretch()

        label = QLabel("Welcome to QuizPy!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setWordWrap(True)
        label.setStyleSheet("""
            font-family: 'Poppins';
            font-size: 28px;
            color: white;
            font-weight: bold;
        """)
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

        button = QPushButton("Start")
        button.clicked.connect(self.open_auth)
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        self.setLayout(layout)

    # Registratie-/loginpagina starten
    def open_auth(self):
        self.auth_window = AuthWindow()
        self.auth_window.showFullScreen()
        self.hide()

    # Programma afsluiten als de gebruiker op ESC drukt.
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

# Starten van het programma
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartWindow()
    window.showFullScreen()
    sys.exit(app.exec())
