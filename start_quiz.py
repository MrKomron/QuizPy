from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeyEvent
from PyQt6.QtWidgets import QGridLayout, QSpacerItem, QSizePolicy
import json
import os

from level import LevelWindow


class QuizWindow(QWidget):
    def __init__(self, user):
        super().__init__()

        self.user = user
        self.current_level = user["level"]

        self.setWindowTitle(f"QuizPy — Levels (Ingelogd als {user['username']})")
        self.resize(780, 915)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        title = QLabel("Quiz Levels")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 48px; font-weight: 700; color: white;")
        main_layout.addWidget(title)

        spacer_top = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        main_layout.addItem(spacer_top)

        grid_container = QWidget()
        grid_layout = QGridLayout(grid_container)
        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(30)

        self.level_buttons = []

        for lvl in range(1, 11):
            if lvl <= self.current_level:
                btn = QPushButton(f"Level {lvl}")
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        padding: 16px;
                        font-size: 18px;
                        border-radius: 25px;
                        min-width: 150px;
                        min-height: 50px;
                    }
                    QPushButton:hover {
                        background-color: #45a049;
                    }
                """)
                btn.clicked.connect(lambda _, x=lvl: self.start_level(x))
            else:
                btn = QPushButton(f"🔒 Level {lvl}")
                btn.setEnabled(False)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #444;
                        color: #aaa;
                        padding: 16px;
                        font-size: 18px;
                        border-radius: 25px;
                        min-width: 150px;
                        min-height: 50px;
                    }
                """)

            btn.setFont(QFont("Poppins", 12, QFont.Weight.Bold))
            self.level_buttons.append(btn)

            row = 0 if lvl <= 5 else 1
            col = (lvl - 1) % 5
            grid_layout.addWidget(btn, row, col, alignment=Qt.AlignmentFlag.AlignCenter)

        grid_layout.setRowMinimumHeight(0, 70)
        grid_layout.setRowMinimumHeight(1, 70)

        main_layout.addWidget(grid_container, alignment=Qt.AlignmentFlag.AlignCenter)

        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        main_layout.addItem(spacer_bottom)

        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        main_layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignCenter)

    
    def start_level(self, lvl):
        self.level_window = LevelWindow(lvl)
        self.level_window.showFullScreen()
        self.close()

    def finish_level(self, lvl, score):
        """
        Called wanneer een level is voltooid.
        """

        QMessageBox.information(self, "Level voltooid!", f"Je behaalde {score}/10")

        if score >= 5 and lvl == self.current_level and lvl < 10:

            from database import Database
            db = Database()

            new_lvl = self.current_level + 1
            db.conn.execute("UPDATE users SET level = ? WHERE id = ?", (new_lvl, self.user["id"]))
            db.conn.commit()

            QMessageBox.information(
                self,
                "Level unlocked!",
                f"Level {new_lvl} is nu beschikbaar!"
            )

            self.current_level = new_lvl

            for i, btn in enumerate(self.level_buttons, start=1):
                if i <= self.current_level:
                    btn.setText(f"Level {i} — UNLOCKED")
                    btn.setEnabled(True)
                    btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 12px; font-size: 18px;")


    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)                    
