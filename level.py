# level.py
# Dit behandelt de gameplay per level.

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QKeyEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QHBoxLayout

import json
import os
import random


class LevelWindow(QWidget):
    def __init__(self, level_num, database, parent=None):
        super().__init__()
        self.database = database
        self.parent_window = parent
        self.level_num = level_num
        self.questions = []
        self.shuffled_choices = {}
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

        # JSON data importeren uit questions.json.
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 10 random vragen genereren van het level.
        for level in data.get("levels", []):
            if level.get("level") == self.level_num:
                questions = level.get("questions", [])

                if len(questions) < 10:
                    raise ValueError(f"Level {self.level_num} heeft slechts {len(questions)} vragen (minstens 10 vereist)!")

                random.shuffle(questions)
                self.questions = questions[:10]
                break

    # Opzetten van de pagina.
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

        # Keuzebuttons maken.
        for choice in ["A", "B", "C", "D"]:
            button = QPushButton()
            button.setFont(QFont("Poppins", 14))
            button.clicked.connect(lambda checked, ch=choice: self.check_answer(ch))
            self.choice_buttons[choice] = button
            self.buttons_layout.addWidget(button)

        self.layout.addLayout(self.buttons_layout)

        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback_label.setFont(QFont("Poppins", 12, QFont.Weight.Bold))
        self.layout.addWidget(self.feedback_label)

        self.explanation_label = QLabel("")
        self.explanation_label.setWordWrap(True)
        self.explanation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.explanation_label.setFont(QFont("Poppins", 11))
        self.explanation_label.setStyleSheet("color: #dddddd;")
        self.explanation_label.setVisible(False)
        self.layout.addWidget(self.explanation_label)

        # Buttons aanmaken.
        self.next_button = QPushButton("Volgende Vraag")
        self.next_button.clicked.connect(self.next_question)
        self.next_button.setVisible(False)
        self.layout.addWidget(self.next_button, alignment=Qt.AlignmentFlag.AlignCenter)

        menu_button = QPushButton("Menu")
        menu_button.clicked.connect(self.return_to_levels)
        self.layout.addWidget(menu_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
    def show_question(self):
        # Op het einde het resultaat tonen
        if self.current_question_index >= len(self.questions):
            self.show_result()
            return

        self.time_left = self.time_per_question
        self.timer_label.setText(f"Tijd: {self.time_left}s")
        self.timer.start()

        self.feedback_label.setText("")
        self.explanation_label.setVisible(False)
        self.next_button.setVisible(False)

        question = self.questions[self.current_question_index]
        self.question_label.setText(f"Vraag {self.current_question_index + 1}/10: {question['question']}")

        # De keuzes in een willekeurige volgorde zetten.
        choices = list(question["choices"].items())
        random.shuffle(choices)

        self.shuffled_choices = {}
        for button_key, (original_key, text) in zip(self.choice_buttons.keys(), choices):
            button = self.choice_buttons[button_key]
            button.setText(f"{text}")
            button.setEnabled(True)
            button.setStyleSheet("")
            
            self.shuffled_choices[button_key] = original_key

        self.inverse_shuffled_choices = {v: k for k, v in self.shuffled_choices.items()}

    def check_answer(self, selected_choice):
        self.timer.stop()
        question = self.questions[self.current_question_index]
        correct_choice = question["correct_answer"]

        for button in self.choice_buttons.values():
            button.setEnabled(False)

        choice = self.shuffled_choices[selected_choice]
        # Juist antwoord.
        if choice == correct_choice:
            self.score += 1
            self.feedback_label.setText("Correct! 🎉")
            self.choice_buttons[selected_choice].setStyleSheet("background-color: #4CAF50; color: white;")

        # Fout antwoord.
        else:
            correct_choice = self.inverse_shuffled_choices[correct_choice]
            self.feedback_label.setText(f"Fout! Het juiste antwoord was {correct_choice}.")
            self.choice_buttons[selected_choice].setStyleSheet("background-color: #f44336; color: white;")
            self.choice_buttons[correct_choice].setStyleSheet("background-color: #4CAF50; color: white;")

        explanation = question.get("explanation", "")
        if explanation:
            self.explanation_label.setText(f"ℹ️ {explanation}")
            self.explanation_label.setVisible(True)

        # Checken of het de laatste vraag is.
        if self.current_question_index == len(self.questions) - 1:
            self.next_button.setText("Verdergaan")

        self.next_button.setVisible(True)

    def next_question(self):
        # Resultaat tonen als het de laatste vraag was.
        if self.current_question_index == len(self.questions) - 1:
            self.show_result()
            return

        self.current_question_index += 1
        self.show_question()

    def show_result(self):
        self.timer.stop()
        self.timer_label.setText("")

        for button in self.choice_buttons.values():
            button.setVisible(False)

        self.explanation_label.setVisible(False)
        
        self.question_label.setText(f"Je hebt {self.score} van de {len(self.questions)} vragen goed beantwoord!")
        self.feedback_label.setText("")

        if self.parent_window:
            self.parent_window.finish_level(self.level_num, self.score)

        self.next_button.setText("Terug naar Levels")
        self.next_button.clicked.disconnect()
        self.next_button.clicked.connect(self.return_to_levels)
        self.next_button.setVisible(True)

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f"Tijd: {self.time_left}s")

        if self.time_left <= 0:
            self.timer.stop()

            if self.current_question_index == len(self.questions) - 1:
                self.show_result()
            else:
                self.next_question()

    # Terugkeren naar menu.
    def return_to_levels(self):
        if self.parent_window:
            self.parent_window.showFullScreen()
            
        self.close()

    # Programma afsluiten als de gebruiker op ESC drukt.
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
