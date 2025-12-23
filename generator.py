import random
import json
from db import get_conn

def get_questions(subject, limit):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT question, options, correct
    FROM questions
    WHERE subject=?
    ORDER BY RANDOM()
    LIMIT ?
    """, (subject, limit))

    rows = cur.fetchall()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "question": r[0],
            "options": json.loads(r[1]),
            "correct": r[2]
        })
    return result

def generate_test(main1, main2):
    test = []
    test += get_questions("Ona tili", 10)
    test += get_questions("Matematika", 10)
    test += get_questions("Tarix", 10)
    test += get_questions(main1, 30)
    test += get_questions(main2, 30)
    return test
