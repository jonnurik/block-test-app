# importer.py
import pandas as pd
from db import insert_question


def import_excel(path, subject, block):
    df = pd.read_excel(path)

    required_cols = ["Savol", "A", "B", "C", "D", "Togri", "Qiyinlik"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Ustun topilmadi: {col}")

    count = 0

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
        count += 1

    return count
