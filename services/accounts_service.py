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
                society_id, ac_no, name, header,
                parent_ac_no, dr_cr_type,
                bf_flag, bf_value, depreciation, tab
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            society_id,
            row['Ac No'],
            row['Name'],
            row['Header'],
            row['Hierarchy'],
            row['DrCrAc'],
            row['B/F?'],
            row['B/F'],
            row['Depreciation'],
            row['Tab']
        ))

    db.commit()
    cur.close()
    db.close()

    return "Accounts Uploaded"