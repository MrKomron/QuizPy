from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class QuizWindow(QWidget):
    def __int__(self):
        super().__init__()
        self.setWindowTitle("QuizPy - Quiz")
        self.resize(780,915)

        layout=QVBoxLayout(self)
        title =QLabel("Quiz gestart!")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: 700; color: white;")
        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
