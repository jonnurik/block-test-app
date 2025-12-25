def get_questions(subject, block_type):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, question, A, B, C, D, correct, difficulty
        FROM questions
        WHERE subject=? AND block_type=?
        ORDER BY id DESC
    """, (subject, block_type))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_stats_filtered(subject, block_type):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM questions
        WHERE subject=? AND block_type=?
    """, (subject, block_type))
    count = cur.fetchone()[0]
    conn.close()
    return count
