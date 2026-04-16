from flask import Flask
from dash import Dash, dcc
import os
from ui.layout import serve_layout
from ui.callbacks.auth_callbacks import register_auth_callbacks
from ui.callbacks.admin_callbacks import register_admin_callbacks
from ui.callbacks.security_callbacks import register_security_callbacks
from ui.callbacks.jwt_callbacks import register_jwt_callbacks
from dotenv import load_dotenv
from auth.routes import auth_bp

load_dotenv()

server = Flask(__name__)
server.secret_key = os.getenv("SECRET_KEY")
server.register_blueprint(auth_bp, url_prefix="/auth")

app = Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True
)

# Add push.js to layout
from dash import html
original_layout = serve_layout()
if isinstance(original_layout.children, list):
    original_layout.children.append(html.Script(src="/assets/push.js"))

app.layout = original_layout

register_auth_callbacks(app)
register_admin_callbacks(app)
register_security_callbacks(app)
register_jwt_callbacks(app)

server = app.server

if __name__ == "__main__":
    app.run_server(debug=False, host="127.0.0.1", port=8050)