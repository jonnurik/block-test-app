import json
from db import insert

def import_json(path, subject, block_type):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    count = 0
    for q in data:
        answers = q["answers"]
        correct = ""
        for a in answers:
            if a.get("correct") == "1":
                correct = a["answer"]

        insert((
            subject,
            block_type,
            q.get("difficulty","orta"),
            q["question"],
            answers[0]["answer"],
            answers[1]["answer"],
            answers[2]["answer"],
            answers[3]["answer"],
            correct
        ))
        count += 1
    return count
