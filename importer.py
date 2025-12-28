# importer.py
import pandas as pd
from db import insert_question


def import_xlsx(path, subject, block):
    """
    Excel ustunlari SHART:
    Savol | A | B | C | D | Togri | Qiyinlik
    """

    df = pd.read_excel(path)

    required_cols = ["Savol", "A", "B", "C", "D", "Togri", "Qiyinlik"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Excel faylda '{col}' ustuni topilmadi")

    added = 0

    for _, row in df.iterrows():
        insert_question(
            subject=subject,
            block=block,
            q=str(row["Savol"]),
            a=str(row["A"]),
            b=str(row["B"]),
            c=str(row["C"]),
            d=str(row["D"]),
            correct=str(row["Togri"]),
            difficulty=str(row["Qiyinlik"])
        )
        added += 1

    return added
