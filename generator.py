from db import random_questions


def generate(subject, block, count):
    qs = random_questions(subject, block, count)
    if len(qs) < count:
        raise Exception(f"{subject} ({block}) fanidan savol yetarli emas")
    return qs
