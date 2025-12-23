import sqlite3

DB = "tests.db"

def connect():
    return sqlite3.connect(DB)

def init_db():
    con = connect()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            level TEXT,
            question TEXT,
            A TEXT, B TEXT, C TEXT, D TEXT
        )
    """)
    con.commit()
    con.close()

def insert_many(rows):
    con = connect()
    cur = con.cursor()
    cur.executemany("""
        INSERT INTO questions
        (subject, level, question, A, B, C, D)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, rows)
    con.commit()
    con.close()

def count_by_subject():
    con = connect()
    cur = con.cursor()
    cur.execute("""
        SELECT subject, COUNT(*) FROM questions GROUP BY subject
    """)
    rows = cur.fetchall()
    con.close()
    return dict(rows)

def get_questions(subject, level, limit):
    con = connect()
    cur = con.cursor()
    cur.execute("""
        SELECT question, A, B, C, D
        FROM questions
        WHERE subject=? AND level=?
        ORDER BY RANDOM()
        LIMIT ?
    """, (subject, level, limit))
    data = cur.fetchall()
    con.close()
    return [
        {"q": r[0], "A": r[1], "B": r[2], "C": r[3], "D": r[4]}
        for r in data
    ]
