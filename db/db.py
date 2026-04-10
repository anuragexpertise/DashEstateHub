import os
import psycopg2

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode="require"
    )
# PGHOST='ep-long-frog-a1asxc6t-pooler.ap-southeast-1.aws.neon.tech'
# PGDATABASE='neondb'
# PGUSER='neondb_owner'
# PGPASSWORD='npg_k7mqBcDeMbs5'
# PGSSLMODE='require'
# PGCHANNELBINDING='require'