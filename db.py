import sqlite3
import os
import sys

def get_base_path():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(get_base_path(), "tests.db")

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            block_type TEXT,
            difficulty TEXT,
            question TEXT,
            options TEXT,
            correct TEXT
        )
    """)
    conn.commit()
    conn.close()
