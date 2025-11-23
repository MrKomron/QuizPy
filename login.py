from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QPushButton, QMessageBox
from database import Database

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()   # HIER wordt quiz.db gemaakt/geopend
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Login")
        layout = QVBoxLayout()

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        btn = QPushButton("Login")
        btn.clicked.connect(self.do_login)

        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(btn)
        self.setLayout(layout)

    def do_login(self):
        user = self.db.get_user(self.username.text(), self.password.text())
        if user:
            QMessageBox.information(self, "Yes", f"Ingelogd als {user['username']}")
        else:
            QMessageBox.warning(self, "Nee", "Verkeerde login")
