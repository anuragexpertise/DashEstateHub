from flask import Flask, session
from dash import Dash, dcc, html
import os
from ui.layout import serve_layout
from ui.callbacks.auth_callbacks import register_auth_callbacks
from ui.callbacks.admin_callbacks import register_admin_callbacks
from ui.callbacks.security_callbacks import register_security_callbacks
from ui.callbacks.jwt_callbacks import register_jwt_callbacks
from dotenv import load_dotenv
from auth.routes import auth_bp
import secrets

load_dotenv()

server = Flask(__name__)
# Use a strong secret key
server.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(32))
# Enable session to be permanent
server.config['SESSION_PERMANENT'] = True
server.config['SESSION_TYPE'] = 'filesystem'
server.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours

server.register_blueprint(auth_bp, url_prefix="/auth")

app = Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    assets_folder='assets'
)

app.layout = serve_layout()

# Register callbacks
register_auth_callbacks(app)
register_admin_callbacks(app)
register_security_callbacks(app)
register_jwt_callbacks(app)

server = app.server

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=8050)