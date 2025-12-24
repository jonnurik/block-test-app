import sqlite3
import os

def get_db_path():
    base = os.path.join(os.path.expanduser("~"), "Documents", "BlockTestGenerator")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "tests.db")

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

def get_questions_by_subject(subject):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    SELECT id, question, A, B, C, D, correct
    FROM questions
    WHERE subject=?
    ORDER BY id DESC
    """, (subject,))
    rows = cur.fetchall()
    conn.close()
    return rows

def update_question(qid, q, A, B, C, D, correct):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    UPDATE questions
    SET question=?, A=?, B=?, C=?, D=?, correct=?
    WHERE id=?
    """, (q, A, B, C, D, correct, qid))
    conn.commit()
    conn.close()

def delete_question(qid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM questions WHERE id=?", (qid,))
    conn.commit()
    conn.close()

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
    return [{"q": r[0], "A": r[1], "B": r[2], "C": r[3], "D": r[4]} for r in rows]
