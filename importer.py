import json
from db import add_question


def import_json(path, subject, block):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise Exception("JSON massiv bo‘lishi kerak")

    count = 0
    for q in data:
        add_question(
            subject,
            block,
            q.get("difficulty", "o‘rta"),
            q["question"],
            q["A"],
            q["B"],
            q["C"],
            q["D"],
            q["correct"]
        )
        count += 1

    return count
