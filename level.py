from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QHBoxLayout,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QKeyEvent
import json
import os


class LevelWindow(QWidget):
    def __init__(self, level_num):
        super().__init__()

        self.level_num = level_num
        self.questions = []
        self.current_question_index = 0
        self.score = 0

        self.time_per_question=15
        self.time_left = self.time_per_question
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)

        self.setWindowTitle(f"QuizPy - Level {level_num}")
        self.resize(700, 600)

        self.load_questions()
        self.init_ui()
        self.show_question()

    def load_questions(self):
        json_path = os.path.join(os.path.dirname(__file__), "questions.json")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        levels = data.get("levels", [])
        for lvl in levels:
            if lvl.get("level") == self.level_num:
                self.questions = [q for q in lvl.get("questions", []) if not q.get("is_backup", False)]
                break

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(20)

        self.timer_label = QLabel("Tijd: 15s")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setFont(QFont("Poppins", 14, QFont.Weight.Medium))
        self.layout.addWidget(self.timer_label)

        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setFont(QFont("Poppins", 16, QFont.Weight.Bold))
        self.layout.addWidget(self.question_label)

        self.buttons_layout = QVBoxLayout()
        self.choice_buttons = {}

        for choice in ["A", "B", "C", "D"]:
            btn = QPushButton()
            btn.setFont(QFont("Poppins", 14))
            btn.clicked.connect(lambda checked, ch=choice: self.check_answer(ch))
            self.choice_buttons[choice] = btn
            self.buttons_layout.addWidget(btn)

        self.layout.addLayout(self.buttons_layout)

        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback_label.setFont(QFont("Poppins", 12, QFont.Weight.Bold))
        self.layout.addWidget(self.feedback_label)

        self.next_button = QPushButton("Volgende Vraag")
        self.next_button.clicked.connect(self.next_question)
        self.next_button.setVisible(False)
        self.layout.addWidget(self.next_button, alignment=Qt.AlignmentFlag.AlignCenter)

        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        self.layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
    def show_question(self):
        if self.current_question_index >= len(self.questions):
            self.show_result()
            return

        self.time_left = self.time_per_question
        self.timer_label.setText(f"Tijd: {self.time_left}s")
        self.timer.start()

        self.feedback_label.setText("")
        self.next_button.setVisible(False)

        question = self.questions[self.current_question_index]
        self.question_label.setText(f"Vraag {self.current_question_index + 1}: {question['question']}")

        for choice, btn in self.choice_buttons.items():
            btn.setText(f"{choice}: {question['choices'][choice]}")
            btn.setEnabled(True)
            btn.setStyleSheet("")

    def check_answer(self, selected_choice):
        self.timer.stop()
        question = self.questions[self.current_question_index]
        correct_choice = question["correct_answer"]

        for btn in self.choice_buttons.values():
            btn.setEnabled(False)

        if selected_choice == correct_choice:
            self.score += 1
            self.feedback_label.setText("Correct! 🎉")
            self.choice_buttons[selected_choice].setStyleSheet("background-color: #4CAF50; color: white;")
        else:
            self.feedback_label.setText(f"Fout! Het juiste antwoord was {correct_choice}.")
            self.choice_buttons[selected_choice].setStyleSheet("background-color: #f44336; color: white;")
            self.choice_buttons[correct_choice].setStyleSheet("background-color: #4CAF50; color: white;")

        self.next_button.setVisible(True)

    def next_question(self):
        self.current_question_index += 1
        self.show_question()

    def show_result(self):
        self.timer.stop()
        self.timer_label.setText("")

        for btn in self.choice_buttons.values():
            btn.setVisible(False)
            
        self.question_label.setText(f"Je hebt {self.score} van de {len(self.questions)} vragen goed beantwoord!")
        self.feedback_label.setText("")

        self.next_button.setText("Terug naar Levels")
        self.next_button.clicked.disconnect()
        self.next_button.clicked.connect(self.close)
        self.next_button.setVisible(True)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f"Tijd: {self.time_left}s")

        if self.time_left <= 0:
            # tijd is op → stop timer en skip vraag
            self.timer.stop()
            self.feedback_label.setText("Tijd is op! Vraag wordt overgeslagen.")
            # geen score wijzigen, gewoon naar volgende vraag
            self.next_question()

