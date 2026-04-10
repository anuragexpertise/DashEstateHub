from db import get_db
from werkzeug.security import check_password_hash

def authenticate_user(email, password):

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT id, role, password_hash, society_id, linked_id
        FROM users
        WHERE email = %s AND active = TRUE
    """, (email,))

    user = cur.fetchone()

    cur.close()
    db.close()

    if not user:
        return None

    user_id, role, password_hash, society_id, linked_id = user

    if not check_password_hash(password_hash, password):
        return None

    return {
        "user_id": user_id,
        "role": role,
        "society_id": society_id,
        "linked_id": linked_id
    }