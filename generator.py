from db import random_questions


def generate_blocks(asosiy1, asosiy2):
    blocks = []

    blocks.append(("Ona tili (majburiy)", random_questions("Ona tili", "majburiy", 10)))
    blocks.append(("Matematika (majburiy)", random_questions("Matematika", "majburiy", 10)))
    blocks.append(("Tarix (majburiy)", random_questions("Tarix", "majburiy", 10)))
    blocks.append((asosiy1, random_questions(asosiy1, "asosiy", 30)))
    blocks.append((asosiy2, random_questions(asosiy2, "asosiy", 30)))

    for title, qs in blocks:
        if len(qs) == 0:
            raise Exception(f"{title} fanidan savollar yetarli emas")

    return blocks
