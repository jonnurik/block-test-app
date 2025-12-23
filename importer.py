
import pandas as pd

REQUIRED_COLUMNS = ["subject", "question", "A", "B", "C", "D"]

def load_questions(path):
    if path.endswith(".csv"):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"Ustun yetishmayapti: {col}")

    questions = {}
    for _, r in df.iterrows():
        subject = str(r["subject"]).strip()
        q = {
            "q": str(r["question"]),
            "A": str(r["A"]),
            "B": str(r["B"]),
            "C": str(r["C"]),
            "D": str(r["D"]),
        }
        questions.setdefault(subject, []).append(q)

    return questions
