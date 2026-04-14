from werkzeug.security import generate_password_hash
from db import get_db

MASTER_EMAIL = "master@estatehub.com"
MASTER_PASSWORD = "Master@1234"

db = get_db()
cur = db.cursor()

# Check whether the master admin user already exists
cur.execute("""
    SELECT id, email, role, society_id
    FROM users
    WHERE email = %s
""", (MASTER_EMAIL,))
master_user = cur.fetchone()

hashed_password = generate_password_hash(MASTER_PASSWORD)

if master_user:
    print(f"Updating password for existing master admin: {MASTER_EMAIL}")
    cur.execute("""
        UPDATE users
        SET password_hash = %s
        WHERE email = %s
    """, (hashed_password, MASTER_EMAIL))
else:
    print(f"Creating master admin user: {MASTER_EMAIL}")
    cur.execute("""
        INSERT INTO users (society_id, email, password_hash, role, linked_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (None, MASTER_EMAIL, hashed_password, "admin", None))

db.commit()
cur.close()
db.close()

print("Master admin password set successfully.")

