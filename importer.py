import json
from db import init_db, insert_many

def import_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for q in data:
        rows.append((
            q["subject"],
            q.get("difficulty", "orta"),
            q["question"],
            q["answers"][0],
            q["answers"][1],
            q["answers"][2],
            q["answers"][3],
        ))

    init_db()
    insert_many(rows)

    return len(rows)
