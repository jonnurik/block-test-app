import json
from db import insert_question

def import_json(path, subject, block_type):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    count = 0
    for q in data:
        answers = q.get("answers", [])
        if len(answers) < 4:
            continue

        correct = ""
        for a in answers:
            if a.get("correct") == "1":
                correct = a["answer"]

        if not correct:
            continue

        insert_question((
            subject,
            block_type,
            q.get("difficulty", "orta"),
            q["question"],
            answers[0]["answer"],
            answers[1]["answer"],
            answers[2]["answer"],
            answers[3]["answer"],
            correct
        ))

        count += 1

    return count
