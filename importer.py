import json
from db import insert_question


def import_json(path, subject, block_type):
    """
    JSON format:
    [
      {
        "question": "...",
        "A": "...",
        "B": "...",
        "C": "...",
        "D": "...",
        "correct": "A",
        "difficulty": "oson"
      }
    ]
    """

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            raise ValueError("JSON fayl noto‘g‘ri formatda")

    if not isinstance(data, list):
        raise ValueError("JSON massiv (list) bo‘lishi kerak")

    count = 0

    for i, item in enumerate(data, start=1):
        try:
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
        except KeyError as e:
            raise ValueError(f"{i}-savolda maydon yetishmayapti: {e}")

    return count
