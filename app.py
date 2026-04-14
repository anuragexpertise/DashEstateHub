from flask import Flask
from dash import Dash
import os
from ui.layout import serve_layout
from ui.callbacks.auth_callbacks import register_auth_callbacks
from ui.callbacks.admin_callbacks import register_admin_callbacks
from ui.callbacks.security_callbacks import register_security_callbacks
from dotenv import load_dotenv

load_dotenv()
server = Flask(__name__)
server.secret_key = os.getenv("SECRET_KEY")

app = Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True
)
# -----------------------------
# ✅ ADD DB TEST ROUTE HERE
# -----------------------------
from db import get_db

# @server.route("/test-db")
# def test_db():
#     # return f"""
#     #         Host: {os.getenv('PGHOST')}
#     #         User: {os.getenv('PGUSER')}
#     #         DB: {os.getenv('PGDATABASE')}
#     #         """
#     try:
        
#         db = get_db()
#         cur = db.cursor()

#         cur.execute("SELECT 1;")
#         result = cur.fetchone()

#         cur.close()
#         db.close()

#         return f"DB OK: {result}"

#     except Exception as e:
#         return f"DB ERROR: {str(e)}"

# -----------------------------
# Navbar is now handled by the router callback in auth_callbacks.py
app.layout = serve_layout()

register_auth_callbacks(app)
register_admin_callbacks(app)
register_security_callbacks(app)

server = app.server

if __name__ == "__main__":
    app.run_server(debug=False, host="127.0.0.1", port=8050)