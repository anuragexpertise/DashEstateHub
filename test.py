from werkzeug.security import generate_password_hash
from db import get_db

db = get_db()
cur = db.cursor()

cur.execute("""
    SELECT * FROM users
""")
users = cur.fetchall()
for user in users:
    print(user)
# Example: update one user
# cur.execute("""
#     SELECT users
#     SET password_hash=%s
#     WHERE email=%s
# """, (generate_password_hash("1234"), "master@estatehub.com"))

# db.commit()
cur.close()
db.close()
# print(generate_password_hash("1234"))

