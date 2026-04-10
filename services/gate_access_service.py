from db import get_db
from services.charges_engine import calculate_apartment_dues

def has_open_entry(role, entity_id):
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT * FROM gate_access 
        WHERE role=%s AND entity_id=%s AND time_out IS NULL
    """, (role, entity_id))

    return cur.fetchone()


def create_entry(society_id, role, entity_id):
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO gate_access (society_id, role, entity_id, time_in)
        VALUES (%s,%s,%s,NOW())
    """, (society_id, role, entity_id))


def validate_apartment(apt_id):
    dues = calculate_apartment_dues(apt_id)
    return "PASS" if dues <= 0 else "FAIL"


def handle_scan(society_id, role, entity_id):
    if has_open_entry(role, entity_id):
        return "OPEN ENTRY EXISTS"

    if role == 'O':
        status = validate_apartment(entity_id)
    else:
        status = "PASS"

    if status == "FAIL":
        return "FAIL"

    create_entry(society_id, role, entity_id)
    return "PASS"