from db import get_db

def create_transaction(society_id, entries, description, date):
    db = get_db()
    cur = db.cursor()

    cur.execute(
        "INSERT INTO transactions (society_id, txn_date, description) VALUES (%s,%s,%s)",
        (society_id, date, description)
    )
    txn_id = cur.lastrowid

    total_dr = sum(e['dr'] for e in entries)
    total_cr = sum(e['cr'] for e in entries)

    if total_dr != total_cr:
        raise Exception("Unbalanced transaction")

    for e in entries:
        cur.execute("""
            INSERT INTO ledger_entries 
            (society_id, txn_id, account_number, dr_amount, cr_amount, txn_date)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            society_id,
            txn_id,
            e['account'],
            e['dr'],
            e['cr'],
            date
        ))

    return txn_id


def get_account_balance(account_number):
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT SUM(dr_amount) as dr, SUM(cr_amount) as cr
        FROM ledger_entries
        WHERE account_number=%s
    """, (account_number,))

    row = cur.fetchone()

    return (row['dr'] or 0) - (row['cr'] or 0)