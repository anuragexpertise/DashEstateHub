from db import get_db
from datetime import date

def calculate_apartment_dues(apt_id):
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM apartments WHERE id=%s", (apt_id,))
    apt = cur.fetchone()

    cur.execute("""
        SELECT * FROM charges_fines 
        WHERE apt_id=%s AND apt_status=1
    """, (apt_id,))
    charge = cur.fetchone()

    if not charge:
        return 0

    months = 1  # can expand later

    maintenance = apt['apartment_size'] * charge['apt_maintenance_rate'] * months

    return maintenance