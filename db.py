import sqlite3
import os

DB_DIR = os.path.join(os.path.expanduser("~"), "BlockTestGenerator")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "tests.db")


def connect():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        block TEXT,
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


def add_question(subject, block, difficulty, q, A, B, C, D, correct):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO questions VALUES (NULL,?,?,?,?,?,?,?,?,?)
    """, (subject, block, difficulty, q, A, B, C, D, correct))
    conn.commit()
    conn.close()


def update_question(qid, q, A, B, C, D, correct, difficulty):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    UPDATE questions
    SET question=?, A=?, B=?, C=?, D=?, correct=?, difficulty=?
    WHERE id=?
    """, (q, A, B, C, D, correct, difficulty, qid))
    conn.commit()
    conn.close()


def get_questions(subject, block):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    SELECT id, question, A, B, C, D, correct, difficulty
    FROM questions
    WHERE subject=? AND block=?
    """, (subject, block))
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_question(qid):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM questions WHERE id=?", (qid,))
    conn.commit()
    conn.close()


def clear_block(subject, block):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM questions WHERE subject=? AND block=?", (subject, block))
    conn.commit()
    conn.close()


def get_stats():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    SELECT subject, block, COUNT(*)
    FROM questions
    GROUP BY subject, block
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def random_questions(subject, block, limit):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    SELECT question, A, B, C, D, correct
    FROM questions
    WHERE subject=? AND block=?
    ORDER BY RANDOM()
    LIMIT ?
    """, (subject, block, limit))
    rows = cur.fetchall()
    conn.close()
    return rows
