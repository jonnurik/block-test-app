from db import get_questions

def generate_block(subject, total):
    """
    Berilgan fan uchun:
    oson / o‘rta / qiyin savollardan
    teng taqsimlab total ta savol qaytaradi
    """

    part = total // 3

    questions = []
    questions += get_questions(subject, "oson", part)
    questions += get_questions(subject, "orta", part)
    questions += get_questions(subject, "qiyin", part)

    return questions

