import sqlite3
import os
import sys

def base_path():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(base_path(), "tests.db")

def conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    c = conn()
    cur = c.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        block_type TEXT,
        difficulty TEXT,
        question TEXT,
        A TEXT, B TEXT, C TEXT, D TEXT,
        correct TEXT
    )
    """)
    c.commit()
    c.close()

def insert(row):
    c = conn()
    cur = c.cursor()
    cur.execute("""
    INSERT INTO questions
    (subject, block_type, difficulty, question, A, B, C, D, correct)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, row)
    c.commit()
    c.close()

def update(qid, row):
    c = conn()
    cur = c.cursor()
    cur.execute("""
    UPDATE questions SET
    subject=?, block_type=?, difficulty=?, question=?,
    A=?, B=?, C=?, D=?, correct=?
    WHERE id=?
    """, row + (qid,))
    c.commit()
    c.close()

def get_all(subject=None):
    c = conn()
    cur = c.cursor()
    if subject:
        cur.execute("SELECT * FROM questions WHERE subject=?", (subject,))
    else:
        cur.execute("SELECT * FROM questions")
    rows = cur.fetchall()
    c.close()
    return rows

def stats():
    c = conn()
    cur = c.cursor()
    cur.execute("""
    SELECT subject, block_type, COUNT(*)
    FROM questions
    GROUP BY subject, block_type
    """)
    r = cur.fetchall()
    c.close()
    return r

def select(subject, block_type, level, limit):
    c = conn()
    cur = c.cursor()
    cur.execute("""
    SELECT question,A,B,C,D
    FROM questions
    WHERE subject=? AND block_type=? AND difficulty=?
    ORDER BY RANDOM()
    LIMIT ?
    """, (subject, block_type, level, limit))
    r = cur.fetchall()
    c.close()
    return [{"q":x[0],"A":x[1],"B":x[2],"C":x[3],"D":x[4]} for x in r]
