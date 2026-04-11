from db import get_db

def create_society(data):
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO societies (
            name, address, email, phone,
            secretary_name, secretary_phone,
            plan, plan_validity, arrear_start_date
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (
        data['name'],
        data['address'],
        data['email'],
        data['phone'],
        data['secretary_name'],
        data['secretary_phone'],
        data['plan'],
        data['plan_validity'],
        data['arrear_start_date']
    ))

    society_id = cur.fetchone()[0]
    db.commit()

    cur.close()
    db.close()

    return society_id