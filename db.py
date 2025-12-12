import sqlite3
import os
import random
from typing import List, Dict, Tuple
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "tests.db")

def init_db(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            type TEXT DEFAULT 'main'
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER,
            question TEXT,
            a TEXT, b TEXT, c TEXT, d TEXT,
            correct TEXT,
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        )
    ''')
    conn.commit()
    conn.close()

def get_subject_id(name: str, create_if_missing=True, type_hint: str = 'main') -> int:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM subjects WHERE name = ?", (name,))
    row = c.fetchone()
    if row:
        sid = row[0]
        conn.close()
        return sid
    if create_if_missing:
        c.execute("INSERT INTO subjects (name, type) VALUES (?, ?)", (name, type_hint))
        conn.commit()
        sid = c.lastrowid
        conn.close()
        return sid
    conn.close()
    return None

def add_question(subject_name: str, question: str, a: str, b: str, c: str, d: str, correct: str, type_hint='main'):
    sid = get_subject_id(subject_name, create_if_missing=True, type_hint=type_hint)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO questions (subject_id, question, a, b, c, d, correct)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (sid, question, a, b, c, d, correct.upper()))
    conn.commit()
    conn.close()

def import_questions_from_file(path: str) -> Tuple[int,int]:
    df = None
    ext = os.path.splitext(path)[1].lower()
    if ext in ('.xlsx', '.xls'):
        df = pd.read_excel(path)
    elif ext in ('.csv', '.txt'):
        df = pd.read_csv(path)
    else:
        raise ValueError("Unsupported file type: " + ext)
    df.columns = [c.lower().strip() for c in df.columns]
    required_cols = {'subject', 'question', 'a', 'b', 'c', 'd', 'correct'}
    if not required_cols.issubset(set(df.columns)):
        raise ValueError("Required columns missing. Need: " + ", ".join(required_cols))
    imported = 0
    skipped = 0
    for _, row in df.iterrows():
        try:
            subj = str(row['subject']).strip()
            q = str(row['question']).strip()
            a = str(row['a']).strip()
            b = str(row['b']).strip()
            c = str(row['c']).strip()
            d = str(row['d']).strip()
            correct = str(row['correct']).strip().upper()
            type_hint = 'main'
            if 'type' in df.columns and str(row.get('type','')).strip().lower() == 'mandatory':
                type_hint = 'mandatory'
            if correct not in ('A','B','C','D'):
                skipped += 1
                continue
            add_question(subj, q, a, b, c, d, correct, type_hint=type_hint)
            imported += 1
        except Exception:
            skipped += 1
    return imported, skipped

def list_subjects() -> List[Tuple[int,str,str]]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, name, type FROM subjects ORDER BY name")
    rows = c.fetchall()
    conn.close()
    return rows

def count_questions_by_subject(subject_name: str) -> int:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT COUNT(q.id) FROM questions q
        JOIN subjects s ON q.subject_id = s.id
        WHERE s.name = ?
    ''', (subject_name,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0

def get_questions_for_subject(subject_name: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT q.question, q.a, q.b, q.c, q.d, q.correct
        FROM questions q
        JOIN subjects s ON q.subject_id = s.id
        WHERE s.name = ?
    ''', (subject_name,))
    rows = c.fetchall()
    conn.close()
    return [{'question': r[0], 'a': r[1], 'b': r[2], 'c': r[3], 'd': r[4], 'correct': r[5]} for r in rows]

def get_random_questions(subject_name: str, n: int):
    items = get_questions_for_subject(subject_name)
    import random
    if len(items) <= n:
        random.shuffle(items)
        return items
    return random.sample(items, n)
