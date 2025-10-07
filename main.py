import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from start_quiz import QuizWindow

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("QuizPy")
window.setGeometry(800, 800, 780, 915)
window.setStyleSheet("""
    background-image: url(assets/achtergrond.jpg);
    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;
""")
button=QPushButton("Start")

layout = QVBoxLayout(window)
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
layout.addWidget(button)
button.setStyleSheet("""
    QPushButton {
        color: #ffffff;
        font-family: 'Poppins';
        font-size: 20px;
        font-weight: 700;
        padding: 14px 24px;
        border: none;
        border-radius: 16px;
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:1,
            stop:0 #7C3AED,
            stop:1 #22D3EE
        );
    }

    QPushButton:hover {
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:1,
            stop:0 #8B5CF6,
            stop:1 #67E8F9
        );
    }

    QPushButton:pressed {
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:1,
            stop:0 #6D28D9,
            stop:1 #06B6D4
        );
        padding-top: 16px;
        padding-bottom: 12px;
    }
""")

layout.addStretch()
window.setLayout(layout)

def open_quiz():
    window.quiz=QuizWindow()
    window.quiz.show()
    window.close()
button.clicked.connect(open_quiz)

window.show()
sys.exit(app.exec())
