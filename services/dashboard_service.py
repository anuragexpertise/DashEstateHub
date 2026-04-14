from db import get_db

def get_dashboard_metrics(society_id):
    db = get_db()
    cur= db.cursor()
    try:
        cur.execute("SELECT ...", (society_id,))
        total_dues = cur.fetchone()['dues']
        cur.execute("SELECT ...", (society_id,))
        vendors = cur.fetchone()['count']
        return {"dues": total_dues, "vendors": vendors}
    finally:
        cur.close()
        db.close()      