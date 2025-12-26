import sqlite3
import os

# =====================
# DOIMIY BAZA JOYI
# =====================
BASE_DIR = os.path.join(
    os.path.expanduser("~"),
    "Documents",
    "BlockTestGenerator"
)
os.makedirs(BASE_DIR, exist_ok=True)

DB_PATH = os.path.join(BASE_DIR, "questions.db")


# =====================
# BAZAGA ULANISH
# =====================

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


# =====================
# MAʼLUMOT QO‘SHISH
# =====================

def insert_question(subject, block_type, question, A, B, C, D, correct, difficulty):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO questions
    (subject, block_type, difficulty, question, A, B, C, D, correct)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (subject, block_type, difficulty, question, A, B, C, D, correct))

    conn.commit()
    conn.close()


# =====================
# STATISTIKA (MUHIM!)
# =====================

def get_subject_stats():
    """
    Fan + blok bo‘yicha savollar soni
    """
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


# =====================
# SAVOLLARNI OLISH
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


# =====================
# TEST GENERATSIYA UCHUN
# =====================

def select_questions(subject, block_type, limit):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT question, A, B, C, D
    FROM questions
    WHERE subject=? AND block_type=?
    ORDER BY RANDOM()
    LIMIT ?
    """, (subject, block_type, limit))

    rows = cur.fetchall()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "q": r[0],
            "A": r[1],
            "B": r[2],
            "C": r[3],
            "D": r[4]
        })

    return result


# =====================
# O‘CHIRISH
# =====================

def delete_question(qid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM questions WHERE id=?", (qid,))
    conn.commit()
    conn.close()


def clear_block(subject, block_type):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM questions WHERE subject=? AND block_type=?",
        (subject, block_type)
    )
    conn.commit()
    conn.close()
