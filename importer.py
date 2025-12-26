import json
from db import add_question


def import_json(path, subject, block):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise Exception("JSON massiv (list) bo‘lishi kerak")

    count = 0

    for i, q in enumerate(data, start=1):
        try:
            # 1️⃣ Variantlar 2 xil formatda bo‘lishi mumkin
            if "A" in q:
                A = q["A"]
                B = q["B"]
                C = q["C"]
                D = q["D"]
                correct = q["correct"]
            elif "answers" in q and isinstance(q["answers"], list):
                answers = q["answers"]
                if len(answers) < 4:
                    raise Exception("answers kamida 4 ta bo‘lishi kerak")

                A, B, C, D = answers[:4]

                # correct index → harf
                idx = q.get("correct", 0)
                correct = ["A", "B", "C", "D"][idx]
            else:
                raise Exception("Variantlar topilmadi (A/B/C/D yoki answers yo‘q)")

            add_question(
                subject,
                block,
                q.get("difficulty", "o‘rta"),
                q["question"],
                A, B, C, D,
                correct
            )
            count += 1

        except Exception as e:
            raise Exception(f"{i}-savolda xato: {e}")

    return count