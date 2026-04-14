from db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

def authenticate_user(email, password, society_id=None):
    """
    Authenticate user with email and password.
    Optionally filter by society_id for SaaS multi-tenancy.
    """

    db = get_db()
    cur = db.cursor()

    if email == "master@estatehub.com":
        cur.execute("""
            SELECT id, role, password_hash, society_id, linked_id, login_method
            FROM users
            WHERE email = %s
        """, (email,))
    elif society_id:
        cur.execute("""
            SELECT id, role, password_hash, society_id, linked_id, login_method
            FROM users
            WHERE email = %s AND society_id = %s
        """, (email, society_id))
    else:
        cur.execute("""
            SELECT id, role, password_hash, society_id, linked_id, login_method
            FROM users
            WHERE email = %s
        """, (email,))

    user = cur.fetchone()
    cur.close()
    db.close()

    if not user:
        print("No user found with email:", email)
        return None
    
    if not check_password_hash(user['password_hash'], password):
        print("Invalid password for user:", email)
        return None

    return {
        "user_id": user['id'],
        "role": user['role'],
        "society_id": user['society_id'],
        "linked_id": user['linked_id'],
        "login_method": user['login_method'],
        "email": email
    }


def authenticate_pin(email, pin, society_id=None):
    """
    Authenticate user with email and PIN.
    Optionally filter by society_id for SaaS multi-tenancy.
    """

    db = get_db()
    cur = db.cursor()

    if email == "master@estatehub.com":
        cur.execute("""
            SELECT id, role, pin_hash, society_id, linked_id, login_method
            FROM users
            WHERE email = %s
        """, (email,))
    elif society_id:
        cur.execute("""
            SELECT id, role, pin_hash, society_id, linked_id, login_method
            FROM users
            WHERE email = %s AND society_id = %s
        """, (email, society_id))
    else:
        cur.execute("""
            SELECT id, role, pin_hash, society_id, linked_id, login_method
            FROM users
            WHERE email = %s
        """, (email,))

    user = cur.fetchone()
    cur.close()
    db.close()

    if not user:
        print("No user found for PIN login:", email)
        return None

    if not user['pin_hash'] or not check_password_hash(user['pin_hash'], pin):
        print("Invalid PIN for user:", email)
        return None

    return {
        "user_id": user['id'],
        "role": user['role'],
        "society_id": user['society_id'],
        "linked_id": user['linked_id'],
        "login_method": user['login_method'],
        "email": email
    }


def authenticate_pattern(email, pattern, society_id=None):
    """
    Authenticate user with email and 9-dot pattern.
    Optionally filter by society_id for SaaS multi-tenancy.
    """

    db = get_db()
    cur = db.cursor()

    if email == "master@estatehub.com":
        cur.execute("""
            SELECT id, role, pattern_hash, society_id, linked_id, login_method
            FROM users
            WHERE email = %s
        """, (email,))
    elif society_id:
        cur.execute("""
            SELECT id, role, pattern_hash, society_id, linked_id, login_method
            FROM users
            WHERE email = %s AND society_id = %s
        """, (email, society_id))
    else:
        cur.execute("""
            SELECT id, role, pattern_hash, society_id, linked_id, login_method
            FROM users
            WHERE email = %s
        """, (email,))

    user = cur.fetchone()
    cur.close()
    db.close()

    if not user:
        print("No user found for pattern login:", email)
        return None

    if not user['pattern_hash'] or not check_password_hash(user['pattern_hash'], pattern):
        print("Invalid pattern for user:", email)
        return None

    return {
        "user_id": user['id'],
        "role": user['role'],
        "society_id": user['society_id'],
        "linked_id": user['linked_id'],
        "login_method": user['login_method'],
        "email": email
    }


def get_societies():
    """
    Get list of all societies for selection.
    """
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT id, name, logo
        FROM societies
        ORDER BY name ASC
    """)

    societies = cur.fetchall()
    cur.close()
    db.close()

    return societies


def get_society_details(society_id):
    """
    Get society details including logo and background.
    """
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT id, name, logo, login_background
        FROM societies
        WHERE id = %s
    """, (society_id,))

    society = cur.fetchone()
    cur.close()
    db.close()

    if not society:
        return None

    return {
        "id": society['id'],
        "name": society['name'],
        "logo": society['logo'],
        "background": society['login_background']
    }