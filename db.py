import sqlite3

DB_NAME = "tests.db"

def get_conn():
    return sqlite3.connect(DB_NAME)

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
