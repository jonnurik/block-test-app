from db import select_questions


def generate_block(subject, block_type, count):
    """
    Test bloki yaratish
    """

    questions = select_questions(subject, block_type, count)

    if len(questions) < count:
        raise Exception(
            f"{subject} ({block_type}) fanidan yetarli savol yo‘q "
            f"({len(questions)}/{count})"
        )

    return questions
