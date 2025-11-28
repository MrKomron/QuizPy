# auth.py

import sqlite3
from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QVBoxLayout, QPushButton,
    QLabel, QMessageBox
)
from PyQt6.QtCore import Qt

from database import Database
from start_quiz import QuizWindow


class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login / Register - QuizPy")
        self.setMinimumSize(400, 300)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(12)

        main_layout.addStretch()
        
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setSpacing(12)
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Login of registreer om verder te gaan")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-family: 'Poppins';
            font-size: 20px;
            font-weight: bold;
        """)
        center_layout.addWidget(title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Gebruikersnaam")
        center_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Wachtwoord")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        center_layout.addWidget(self.password_input)

        self.login_button = QPushButton("Inloggen")
        self.login_button.clicked.connect(self.handle_login)
        center_layout.addWidget(self.login_button)

        self.register_button = QPushButton("Registreren")
        self.register_button.clicked.connect(self.handle_register)
        center_layout.addWidget(self.register_button)

        main_layout.addWidget(center_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addStretch()
        
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        main_layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)


    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Fout", "Vul zowel gebruikersnaam als wachtwoord in.")
            return

        user = self.db.get_user(username, password)

        if user:
            QMessageBox.information(self, "Welkom", f"Ingelogd als {user['username']}")
            self.open_quiz(user)
        else:
            QMessageBox.warning(self, "Fout", "Ongeldige gebruikersnaam of wachtwoord.")

    def handle_register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Fout", "Vul zowel gebruikersnaam als wachtwoord in.")
            return

        try:
            self.db.add_user(username, password)
            QMessageBox.information(self, "OK", "Account aangemaakt! Je kunt nu inloggen.")
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Fout", "Gebruikersnaam bestaat al.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Er ging iets mis:\n{e}")

    def open_quiz(self, user_row):
        """
        user_row is een sqlite3.Row, bv:
        user_row["id"], user_row["username"], user_row["highscore"]
        """
        
        self.quiz_window = QuizWindow(user_row)
        self.quiz_window.showFullScreen()
        self.close()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
