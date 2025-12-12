def import_questions_from_file(path: str, force_subject: str = None, force_type: str = None) -> Tuple[int,int]:
    """
    Import questions from CSV/XLSX file.
    If force_subject is provided, every row will be assigned to that subject (useful when uploading per-block files).
    If force_type is provided, sets the subject type (e.g. 'mandatory' or 'main') for created subject.
    Returns (imported_count, skipped_count).
    """
    df = None
    ext = os.path.splitext(path)[1].lower()
    if ext in ('.xlsx', '.xls'):
        df = pd.read_excel(path)
    elif ext in ('.csv', '.txt'):
        df = pd.read_csv(path)
    else:
        raise ValueError("Unsupported file type: " + ext)

    # normalize columns to lowercase for flexibility
    df.columns = [c.lower().strip() for c in df.columns]

    required_cols = {'question', 'a', 'b', 'c', 'd', 'correct'}
    # 'subject' is optional now because we support force_subject
    if not required_cols.issubset(set(df.columns)):
        # if subject missing but we have force_subject, continue; otherwise error
        if force_subject is None:
            raise ValueError("Required columns missing. Need: " + ", ".join(required_cols))
    imported = 0
    skipped = 0
    for _, row in df.iterrows():
        try:
            subj = force_subject if force_subject is not None else str(row.get('subject','')).strip()
            if not subj:
                # if still empty, skip
                skipped += 1
                continue
            q = str(row['question']).strip()
            a = str(row['a']).strip()
            b = str(row['b']).strip()
            c = str(row['c']).strip()
            d = str(row['d']).strip()
            correct = str(row['correct']).strip().upper()
            type_hint = force_type if force_type is not None else ('mandatory' if str(row.get('type','')).strip().lower() == 'mandatory' else 'main')
            if correct not in ('A','B','C','D'):
                skipped += 1
                continue
            add_question(subj, q, a, b, c, d, correct, type_hint=type_hint)
            imported += 1
        except Exception:
            skipped += 1
    return imported, skipped
