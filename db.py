import sqlite3
import os

def get_db_path():
    home = os.path.expanduser("~")
    data_dir = os.path.join(home, "Documents", "BlockTestGenerator")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "tests.db")

DB_PATH = get_db_path()

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

def insert_question(row):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO questions
    (subject, block_type, difficulty, question, A, B, C, D, correct)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, row)
    conn.commit()
    conn.close()

def get_stats():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    SELECT subject, block_type, COUNT(*)
    FROM questions
    GROUP BY subject, block_type
    ORDER BY subject
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def select_questions(subject, block_type, difficulty, limit):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    SELECT question, A, B, C, D
    FROM questions
    WHERE subject=? AND block_type=? AND difficulty=?
    ORDER BY RANDOM()
    LIMIT ?
    """, (subject, block_type, difficulty, limit))
    rows = cur.fetchall()
    conn.close()
    return [
        {"q": r[0], "A": r[1], "B": r[2], "C": r[3], "D": r[4]}
        for r in rows
    ]
