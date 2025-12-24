import sqlite3
import os

BASE_DIR = os.path.join(
    os.path.expanduser("~"),
    "Documents",
    "BlockTestGenerator"
)

os.makedirs(BASE_DIR, exist_ok=True)

DB_PATH = os.path.join(BASE_DIR, "tests.db")

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
        A TEXT,
        B TEXT,
        C TEXT,
        D TEXT,
        correct TEXT
    )
    """)
    conn.commit()
    conn.close()
