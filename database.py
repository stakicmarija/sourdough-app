import sqlite3
from datetime import datetime

DATABASE_NAME = "sourdough.db"

def get_connection():
    return sqlite3.connect(DATABASE_NAME)

def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS breads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date Text,
            notes TEXT,
            feedback TEXT,
            image_path TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_bread(notes, feedback, image_path):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO breads (date, notes, feedback, image_path)
        VALUES (?, ?, ?, ?)
    """, (datetime.now().isoformat(), notes, feedback, image_path))

    connection.commit()
    connection.close()

def get_all_breads():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM breads")
    breads = cursor.fetchall()

    connection.close()
    return breads



