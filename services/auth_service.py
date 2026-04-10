from db import get_db
from utils.hash_utils import verify_password

def login_email(email, password):
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()

    if user and verify_password(password, user['password_hash']):
        return user

    return None


def login_pin(user_id, pin_hash_input):
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cur.fetchone()

    if user and user['pin_hash'] == pin_hash_input:
        return user

    return None