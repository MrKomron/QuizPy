# # main_old.py
# import sys
# from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
# from PyQt6.QtCore import Qt
#
# from auth import AuthWindow  # <-- nieuw
#
# class StartWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.init_ui()
#
#     def init_ui(self):
#         self.setWindowTitle("QuizPy")
#         self.setGeometry(800, 800, 780, 915)
#         self.setStyleSheet("""
#             QWidget {
#                 background-image: url(assets/achtergrond.jpg);
#                 background-repeat: no-repeat;
#                 background-position: center;
#                 background-size: cover;
#             }
#         """)
#
#         layout = QVBoxLayout()
#         layout.setContentsMargins(24, 24, 24, 24)
#         layout.addStretch()
#
#         label = QLabel("Welcome to QuizPy!")
#         label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         label.setWordWrap(True)
#         label.setStyleSheet("""
#             font-family: 'Poppins';
#             font-size: 28px;
#             color: white;
#             font-weight: bold;
#         """)
#         layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
#
#         button = QPushButton("Start")
#         # (je style van eerder kan je hier 1-op-1 hergebruiken)
#         button.clicked.connect(self.open_auth)
#         layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
#
#         layout.addStretch()
#         self.setLayout(layout)
#
#     def open_auth(self):
#         self.auth_window = AuthWindow()
#         self.auth_window.show()
#         self.close()
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = StartWindow()
#     window.show()
#     sys.exit(app.exec())
