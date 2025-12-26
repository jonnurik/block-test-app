# db.py
import sqlite3
from pathlib import Path

DB_PATH = Path("data.db")


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        block TEXT NOT NULL,
        question TEXT NOT NULL,
        a TEXT,
        b TEXT,
        c TEXT,
        d TEXT,
        correct TEXT,
        difficulty TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_question(subject, block, q, a, b, c, d, correct, difficulty):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO questions
    (subject, block, question, a, b, c, d, correct, difficulty)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (subject, block, q, a, b, c, d, correct, difficulty))

    conn.commit()
    conn.close()


def get_questions(subject, block):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT id, question, a, b, c, d, correct, difficulty
    FROM questions
    WHERE subject=? AND block=?
    """, (subject, block))

    rows = cur.fetchall()
    conn.close()
    return rows


def delete_question(qid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM questions WHERE id=?", (qid,))
    conn.commit()
    conn.close()


def clear_block(subject, block):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM questions WHERE subject=? AND block=?",
        (subject, block)
    )
    conn.commit()
    conn.close()


def get_subject_stats():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT subject, block, COUNT(*)
    FROM questions
    GROUP BY subject, block
    """)

    rows = cur.fetchall()
    conn.close()
    return rows
