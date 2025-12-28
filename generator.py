# generator.py
from db import random_questions


def generate_block(subject, count, block_type=None):
    """
    subject: fan nomi
    count: nechta savol
    block_type: 'majburiy' yoki 'asosiy'
    """
    if block_type is None:
        block_type = "asosiy"

    qs = random_questions(subject, block_type, count)

    return qs
