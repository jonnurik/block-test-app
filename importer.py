import pandas as pd
from db import insert_question


def import_xlsx(path):
    """
    Excel fayldan savollarni o‘qib bazaga yozadi
    Kutilgan ustunlar:
    subject | block | question | A | B | C | D | correct | difficulty
    """

    try:
        df = pd.read_excel(path, engine="openpyxl")
    except ImportError:
        raise Exception(
            "openpyxl topilmadi. Iltimos, dasturni qayta build qiling."
        )

    required_cols = [
        "subject", "block", "question",
        "A", "B", "C", "D", "correct", "difficulty"
    ]

    for col in required_cols:
        if col not in df.columns:
            raise Exception(f"Excel ustuni yetishmayapti: {col}")

    count = 0
    for _, row in df.iterrows():
        insert_question(
            subject=row["subject"],
            block=row["block"],
            question=row["question"],
            a=row["A"],
            b=row["B"],
            c=row["C"],
            d=row["D"],
            correct=row["correct"],
            difficulty=row["difficulty"]
        )
        count += 1

    return count
