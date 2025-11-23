# auth_window.py
import sqlite3
from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QVBoxLayout, QPushButton,
    QLabel, QMessageBox
)
from PyQt6.QtCore import Qt

from database import Database
from start_quiz import QuizWindow  # jouw quizwindow


class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()   # hier maak je de DB-verbinding
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login / Register - QuizPy")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("Login of registreer om verder te gaan")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-family: 'Poppins';
            font-size: 20px;
            font-weight: bold;
        """)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Gebruikersnaam")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Wachtwoord")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Inloggen")
        self.register_button = QPushButton("Registreren")

        # Knoppen stylen kun je later net zo mooi maken als op je startscherm :)
        self.login_button.clicked.connect(self.handle_login)
        self.register_button.clicked.connect(self.handle_register)

        layout.addWidget(title)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Fout", "Vul zowel gebruikersnaam als wachtwoord in.")
            return

        user = self.db.get_user(username, password)

        if user:
            QMessageBox.information(self, "Welkom", f"Ingelogd als {user['username']}")
            # Open de quiz en geef eventueel user-info mee
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
            # Dit gebeurt als username niet uniek is (UNIQUE constraint)
            QMessageBox.warning(self, "Fout", "Gebruikersnaam bestaat al.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Er ging iets mis:\n{e}")

    def open_quiz(self, user_row):
        """
        user_row is een sqlite3.Row, bv:
        user_row["id"], user_row["username"], user_row["highscore"]
        """
        # Hier kun je jouw QuizWindow aanpassen zodat hij bv. user_id meekrijgt:
        # self.quiz_window = QuizWindow(user_row["id"])
        self.quiz_window = QuizWindow()  # als je nog geen user-id verwerkt
        self.quiz_window.show()
        self.close()
