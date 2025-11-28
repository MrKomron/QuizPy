# database.py

import sqlite3
from locale import currency


class Database:
    def __init__(self,path="quiz.db"):
        self.conn=sqlite3.connect(path)
        self.conn.row_factory=sqlite3.Row
        self.create_tables()

    def create_tables(self):
        current=self.conn.cursor()
        current.execute("""
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        highscore INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1
        )
        """)
        self.conn.commit()

    def add_user(self,username, password):
        current=self.conn.cursor()
        current.execute("INSERT INTO users (username,password) VALUES (?,?)",(username, password))
        self.conn.commit()

    def get_user(self,username, password):
        current=self.conn.cursor()
        current.execute("SELECT * FROM users WHERE username = ? AND password  = ?", (username, password))
        return current.fetchone()

    def update_highscore(self, user_id, score):
        current=self.conn.cursor()
        current.execute("UPDATE users SET highscore = ? WHERE id = ?", (score,user_id))
        self.conn.commit()
