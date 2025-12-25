import random
from db import get_questions


def generate_block(subject, block_type, limit):
    rows = get_questions(subject, block_type)
    if len(rows) < limit:
        return []

    random.shuffle(rows)
    return rows[:limit]
