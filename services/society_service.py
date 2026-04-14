from db import get_db
from werkzeug.security import generate_password_hash


# =========================================
# MAIN ENGINE
# =========================================
def create_society_full(data):

    db = get_db()
    cur = db.cursor()

    try:
        # -----------------------------
        # 1. CREATE SOCIETY
        # -----------------------------
        cur.execute("""
            INSERT INTO societies (
                name, address, email, phone,
                secretary_name, secretary_phone,
                plan, plan_validity
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING id
        """, (
            data["name"],
            data.get("address"),
            data.get("email"),
            data.get("phone"),
            data.get("sec_name"),
            data.get("sec_phone"),
            "Free",
            data.get("validity")
        ))

        society_id = cur.fetchone()[0]

        # -----------------------------
        # 2. CREATE ADMIN USER
        # -----------------------------
        password_hash = generate_password_hash(data["admin_password"])

        cur.execute("""
            INSERT INTO users (
                society_id, email, password_hash, role
            )
            VALUES (%s,%s,%s,'admin')
        """, (
            society_id,
            data["admin_email"],
            password_hash
        ))

        # -----------------------------
        # 3. CREATE DEFAULT ACCOUNTS
        # -----------------------------
        create_default_accounts(cur, society_id)

        db.commit()

        return {"status": "success", "society_id": society_id}

    except Exception as e:
        db.rollback()
        print("SOCIETY ERROR:", e)
        return {"status": "error", "message": str(e)}

    finally:
        cur.close()
        db.close()


# =========================================
# DEFAULT CHART OF ACCOUNTS
# =========================================
def create_default_accounts(cur, society_id):

    accounts = [
        ("Cash", "Assets", "Dr"),
        ("Bank", "Assets", "Dr"),
        ("Maintenance Receivable", "Assets", "Dr"),
        ("Maintenance Income", "Income", "Cr"),
        ("Vendor Payments", "Expense", "Dr"),
        ("Penalty Income", "Income", "Cr")
    ]

    for name, tab, drcr in accounts:
        cur.execute("""
            INSERT INTO accounts (
                society_id, name, tab_name, drcr_account
            )
            VALUES (%s,%s,%s,%s)
        """, (society_id, name, tab, drcr))


# =========================================
# FETCH SOCIETIES
# =========================================
def get_societies():

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT id, name, city, created_at
        FROM societies
        ORDER BY id DESC
    """)

    rows = cur.fetchall()

    cur.close()
    db.close()

    return rows

def get_society_details(society_id):

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT id, name, email, phone, address, logo, background
        FROM societies
        WHERE id = %s
    """, (society_id,))

    row = cur.fetchone()
    if not row:
        raise ValueError(f"Society {society_id} not found")

    cur.close()
    db.close()

    return row