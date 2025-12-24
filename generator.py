from db import select_questions

def generate_block(subject, block_type, total):
    part = total // 3
    return (
        select_questions(subject, block_type, "oson", part) +
        select_questions(subject, block_type, "orta", part) +
        select_questions(subject, block_type, "qiyin", part)
    )
