import sqlite3
import os

DB_FILE = "questions.db"


def get_conn():
    return sqlite3.connect(DB_FILE)


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        block_type TEXT,
        question TEXT,
        A TEXT,
        B TEXT,
        C TEXT,
        D TEXT,
        correct TEXT,
        difficulty TEXT
    )
    """)

    conn.commit()
    conn.close()


# =====================
# INSERT
# =====================
def insert_question(subject, block_type, q, A, B, C, D, correct, difficulty):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO questions
        (subject, block_type, question, A, B, C, D, correct, difficulty)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (subject, block_type, q, A, B, C, D, correct, difficulty))
    conn.commit()
    conn.close()


# =====================
# SELECT
# =====================
def get_questions(subject, block_type):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, question, A, B, C, D, correct, difficulty
        FROM questions
        WHERE subject=? AND block_type=?
        ORDER BY id DESC
    """, (subject, block_type))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_stats_filtered(subject, block_type):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM questions
        WHERE subject=? AND block_type=?
    """, (subject, block_type))
    count = cur.fetchone()[0]
    conn.close()
    return count


# =====================
# UPDATE
# =====================
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


# =====================
# DELETE
# =====================
def delete_question(qid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM questions WHERE id=?", (qid,))
    conn.commit()
    conn.close()


def clear_questions(subject, block_type):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM questions
        WHERE subject=? AND block_type=?
    """, (subject, block_type))
    conn.commit()
    conn.close()
