from werkzeug.security import generate_password_hash
from db import get_db

db = get_db()
cur = db.cursor()

# Example: update one user
cur.execute("""
    UPDATE users
    SET password_hash=%s
    WHERE email=%s
""", (generate_password_hash("1234"), "admin@estatehub.com"))

db.commit()
cur.close()
db.close()