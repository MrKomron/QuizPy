# menu.py
# Dit behandelt het menu van de game.

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeyEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QGridLayout, QSpacerItem, QSizePolicy

from database import Database
from level import LevelWindow

import json
import os


class QuizWindow(QWidget):
    def __init__(self, user, database):
        super().__init__()
        self.database = database
        
        # Gebruiker en level ophalen.
        self.user = user
        self.current_level = user["level"]

        # Highscores ophalen.
        self.highscores = {}
        for row in self.database.get_statistics(self.user["id"]):
            self.highscores[row["level"]] = row["highscore"]

        self.setWindowTitle(f"QuizPy — Levels (Ingelogd als {user['username']})")
        self.resize(780, 915)

        self.init_ui()

    # Opzetten van de pagina.
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Titel
        title = QLabel("Quiz Levels")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 48px; font-weight: 700; color: white;")
        main_layout.addWidget(title)

        spacer_top = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        main_layout.addItem(spacer_top)

        # Levels tonen in 2 rijen van 5 kolommen.
        grid_container = QWidget()
        grid_layout = QGridLayout(grid_container)
        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(30)

        # Aanmaken van de level buttons.
        self.level_buttons = []
        for level in range(1, 11):
            highscore = self.highscores.get(level)

            # Als level unlocked is.
            if level <= self.current_level:
                if highscore is not None:
                    score_text = f"🎯 {highscore}/10"
                else:
                    score_text = "🎯 0/10"
                
                text = f"Level {level}\n{score_text}"

                button = QPushButton(text)
                button.setFixedSize(180, 60)
                button.setFont(QFont("Poppins", 12, QFont.Weight.Bold))
                self.setup_level_button(button, level)

            # Als level nog niet unlocked is.
            else:
                button = QPushButton(f"🔒 Level {level}")
                button.setFixedSize(180, 60)
                button.setFont(QFont("Poppins", 12, QFont.Weight.Bold))
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #444444;
                        color: #aaa;
                        padding: 8px 16px;
                        font-size: 16px;
                        border-radius: 25px;
                        min-width: 150px;
                        min-height: 60px;
                        text-align: center;
                    }
                """)

            self.level_buttons.append(button)

            if level <= 5:
                row = 0
            else:
                row = 1
                
            column = (level - 1) % 5
            grid_layout.addWidget(button, row, column, alignment=Qt.AlignmentFlag.AlignCenter)

        grid_layout.setRowMinimumHeight(0, 70)
        grid_layout.setRowMinimumHeight(1, 70)

        main_layout.addWidget(grid_container, alignment=Qt.AlignmentFlag.AlignCenter)

        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        main_layout.addItem(spacer_bottom)


        # Afsluit- en Uitlogbuttons.
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        width, height = 120, 40

        exit_button = QPushButton("Afsluiten")
        exit_button.setFixedSize(width, height)
        exit_button.clicked.connect(self.close)
        button_layout.addWidget(exit_button)

        logout_button = QPushButton("Log uit")
        logout_button.setFixedSize(width, height)
        logout_button.clicked.connect(self.logout)
        button_layout.addWidget(logout_button)

        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        main_layout.addWidget(button_widget, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def start_level(self, level):
        self.level_window = LevelWindow(level, self.database, self)
        self.level_window.showFullScreen()
        self.hide()

    def finish_level(self, level, score):
        # Score opslaan
        self.database.save_level_score(self.user["id"], level, score)

        # Highscores opnieuw ophalen
        self.highscores = {}
        for row in self.database.get_statistics(self.user["id"]):
            self.highscores[row["level"]] = row["highscore"]

        # Nieuw level unlocken als score 5 of hoger is.
        if score >= 5 and level == self.current_level and level < 10:
            self.current_level += 1

            self.database.connection.execute("UPDATE users SET level = ? WHERE id = ?", (self.current_level, self.user["id"]))
            self.database.connection.commit()

            QMessageBox.information(self, "Level voltooid", f"Level {self.current_level} is nu beschikbaar!")

        # Buttons updaten.
        for lvl, button in enumerate(self.level_buttons, start=1):
            if lvl <= self.current_level:
                self.setup_level_button(button, lvl)

    # Functie om nieuw unlocked level goed te zetten
    def setup_level_button(self, button, level):
        highscore = self.highscores.get(level)

        if highscore is not None:
            score_text = f"🎯 {highscore}/10"
        else:
            score_text = "🎯 0/10"

        text = f"Level {level}\n{score_text}"

        button.setText(text)
        button.setFixedSize(180, 60)
        button.setEnabled(True)
        button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                font-size: 16px;
                border-radius: 25px;
                min-width: 150px;
                min-height: 60px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        try:
            button.clicked.disconnect()
        except TypeError:
            pass

        button.clicked.connect(lambda _, x=level: self.start_level(x))

    def logout(self):
        from auth import AuthWindow

        self.close()
        self.auth_window = AuthWindow()
        self.auth_window.showFullScreen()

    # Programma afsluiten als de gebruiker op ESC drukt.
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
