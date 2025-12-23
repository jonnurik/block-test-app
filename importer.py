import json
from db import get_conn

def import_json(file_path, subject, block_type, difficulty):
    conn = get_conn()
    cur = conn.cursor()

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for q in data:
        question_text = q["question"]
        answers = q["answers"]

        options = []
        correct = ""

        for a in answers:
            options.append(a["answer"])
            if a["correct"] == "1":
                correct = a["answer"]

        cur.execute("""
        INSERT INTO questions(subject, block_type, difficulty, question, options, correct)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            subject,
            block_type,
            difficulty,
            question_text,
            json.dumps(options, ensure_ascii=False),
            correct
        ))

    conn.commit()
    conn.close()
