# database.py
# Dit behandelt alles in verband met de database (accounts en hun data).

import sqlite3


class Database:
    def __init__(self,path="quiz.db"):
        self.connection=sqlite3.connect(path)
        self.connection.row_factory=sqlite3.Row
        self.create_tables()

    def create_tables(self):
        current=self.connection.cursor()

        # Tabellen aanmaken.
        current.execute("""
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        level INTEGER DEFAULT 1
        )
        """)

        current.execute("""
        CREATE TABLE IF NOT EXISTS level_scores (
            user_id INTEGER,
            level INTEGER,
            highscore INTEGER,
            PRIMARY KEY (user_id, level),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
        
        self.connection.commit()

    def add_user(self,username, password):
        current=self.connection.cursor()
        current.execute("INSERT INTO users (username,password) VALUES (?,?)",(username, password))
        self.connection.commit()

    def get_user(self,username, password):
        current=self.connection.cursor()
        current.execute("SELECT * FROM users WHERE username = ? AND password  = ?", (username, password))
        return current.fetchone()

    def save_level_score(self, user_id, level, score):
        current = self.connection.cursor()

        current.execute("""
            SELECT highscore FROM level_scores
            WHERE user_id = ? AND level = ?
        """, (user_id, level))

        row = current.fetchone()

        # Als er nog geen score is voor een bepaald level wordt de highscore sowieso gezet.
        if row is None:
            current.execute("""
                INSERT INTO level_scores (user_id, level, highscore)
                VALUES (?, ?, ?)
            """, (user_id, level, score))
            
        # Als er wel al een score is voor een bepaald level, highscore alleen aanpassen als de score hoger is.
        elif score > row["highscore"]:
            current.execute("""
                UPDATE level_scores
                SET highscore = ?
                WHERE user_id = ? AND level = ?
            """, (score, user_id, level))

        self.connection.commit()

    def get_statistics(self, user_id):
        current = self.connection.cursor()
        current.execute("""
            SELECT level, highscore FROM level_scores WHERE user_id = ?
        """, (user_id,))
        
        return current.fetchall()
