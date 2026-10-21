import sqlite3
from config import DATABASE_NAME


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        );
    """)

    conn.commit()
    conn.close()
