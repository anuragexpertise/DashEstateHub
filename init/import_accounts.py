import pandas as pd
from db import get_db

def import_accounts(file, society_id):
    df = pd.read_excel(file)

    db = get_db()
    cur = db.cursor()

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO accounts (
                society_id, name,tab_name, header,
                parent_ac_id, dr_cr_account,
                has_bf, bf_type, bf_amount, depreciation_percent, is_depreciable
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
                society_id,
            row['Name'],
            row['Tab Name'],
            row['Header'],
            row['Hierarchy'],
            row['DrCrAc'],
            row['B/F?'],
            row['B/F'],
            row['Depreciation%'],
            row['Depreciable?'],
        ))