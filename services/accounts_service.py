import base64
import io
import pandas as pd
from db import get_db

def process_accounts_upload(contents, society_id):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    df = pd.read_excel(io.BytesIO(decoded))

    db = get_db()
    cur = db.cursor()

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO accounts (
                society_id, name,tab_name, header,
                parent_ac_id, dr_cr_account,
                has_bf, bf_type, bf_amount, depreciation_percent, is_depreciable
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
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

    db.commit()
    cur.close()
    db.close()

    return "Accounts Uploaded"