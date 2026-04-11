from db import get_db

def create_society_full(data):
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO societies 
        (name, email, phone, arrear_start_date)
        VALUES (%s,%s,%s,%s)
    """, (
        data['name'],
        data['email'],
        data['phone'],
        data['arrear_start_date']
    ))

    return cur.lastrowid