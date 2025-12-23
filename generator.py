from db import select

def block(subject, block_type, total):
    p = total // 3
    return (
        select(subject, block_type, "oson", p) +
        select(subject, block_type, "orta", p) +
        select(subject, block_type, "qiyin", p)
    )
