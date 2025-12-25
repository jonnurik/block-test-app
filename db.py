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


def get_questions_by_subject(subject):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    SELECT id, question, A, B, C, D, correct, difficulty
    FROM questions
    WHERE subject=?
    ORDER BY id DESC
    """, (subject,))
    rows = cur.fetchall()
    conn.close()
    return rows


def update_question(qid, q, A, B, C, D, correct, difficulty):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    UPDATE questions
    SET question=?, A=?, B=?, C=?, D=?, correct=?, difficulty=?
    WHERE id=?
    """, (q, A, B, C, D, correct, difficulty, qid))
    conn.commit()
    conn.close()


def delete_question(qid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM questions WHERE id=?", (qid,))
    conn.commit()
    conn.close()


def clear_questions(subject, block_type):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM questions WHERE subject=? AND block_type=?",
        (subject, block_type)
    )
    conn.commit()
    conn.close()
