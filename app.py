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

app = Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True
)

app.layout = serve_layout

register_auth_callbacks(app)
register_admin_callbacks(app)
register_security_callbacks(app)

server = app.server

if __name__ == "__main__":
    app.run_server(debug=True, host="127.0.0.1", port=8050)