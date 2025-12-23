import json
from db import get_conn

def import_json(path, subject, block_type="asosiy", difficulty="orta"):
    conn = get_conn()
    cur = conn.cursor()

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    added = 0

    for q in data:
        question_text = q["question"]

        answers = q.get("answers", [])
        if len(answers) < 4:
            continue  # noto‘g‘ri savollarni tashlab ketamiz

        options = []
        correct = ""

        for a in answers:
            options.append(a["answer"])
            if a.get("correct") == "1":
                correct = a["answer"]

        if not correct:
            continue

        cur.execute("""
            INSERT INTO questions
            (subject, block_type, difficulty, question, options, correct)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            subject,
            block_type,
            difficulty,
            question_text,
            json.dumps(options, ensure_ascii=False),
            correct
        ))

        added += 1

    conn.commit()
    conn.close()
    return added
