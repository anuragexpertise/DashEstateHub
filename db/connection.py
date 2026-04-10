import os
import psycopg2

def get_db():
    return psycopg2.connect(
        host=os.getenv("PGHOST"),
        database=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        sslmode="require",
        channel_binding="require"
    )
# PGHOST='ep-long-frog-a1asxc6t-pooler.ap-southeast-1.aws.neon.tech'
# PGDATABASE='neondb'
# PGUSER='neondb_owner'
# PGPASSWORD='npg_k7mqBcDeMbs5'
# PGSSLMODE='require'
# PGCHANNELBINDING='require'