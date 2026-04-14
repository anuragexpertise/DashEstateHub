import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

def get_db():
    return psycopg2.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        dbname=Config.DB_NAME,
        cursor_factory=RealDictCursor
    )