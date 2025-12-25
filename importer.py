import json
from db import insert_question


def import_json(path, subject, block_type):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    count = 0
    for item in data:
        insert_question(
            subject,
            block_type,
            item["question"],
            item["A"],
            item["B"],
            item["C"],
            item["D"],
            item["correct"],
            item.get("difficulty", "o‘rta")
        )
        count += 1

    return count
