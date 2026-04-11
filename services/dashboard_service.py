from db import get_db

def get_dashboard_metrics(society_id):
    db = get_db()
    cur = db.cursor()

    # Example queries (you will refine)
    cur.execute("SELECT COALESCE(SUM(amount),0) FROM transactions WHERE society_id=%s", (society_id,))
    total_dues = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM vendors WHERE society_id=%s", (society_id,))
    vendors = cur.fetchone()[0]

    return {
        "dues": total_dues,
        "vendors": vendors
    }