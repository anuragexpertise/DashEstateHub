import pandas as pd
from db import get_db

def import_accounts(file, society_id):
    df = pd.read_excel(file)

    db = get_db()
    cur = db.cursor()

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO accounts
            (society_id, account_number, name, header, parent_account_number,
             tab_name, drcr_account, has_bf, bf_type, bf_amount,
             depreciation_percent)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            society_id,
            row['Ac No'],
            row['Name'],
            row['Header'],
            row['Hierarchy'],
            row['Tab'],
            row['DrCrAc'],
            row['B/F?'],
            row['DrCrBF'],
            row['B/F'],
            row['Depreciation']
        ))