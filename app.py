from flask import Flask
from dash import Dash

# Layout
from ui.layout import serve_layout

# Callbacks
from ui.callbacks.auth_callbacks import register_callbacks
from ui.callbacks.security_callbacks import register_security_callbacks
from ui.callbacks.admin_callbacks import register_admin_callbacks

# -----------------------
# Flask server
# -----------------------
server = Flask(__name__)

# -----------------------
# Dash app
# -----------------------
app = Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True
)

# -----------------------
# Layout (FUNCTION, not call)
# -----------------------
app.layout = serve_layout

# -----------------------
# Register ALL callbacks
# -----------------------
register_callbacks(app)
register_security_callbacks(app)
register_admin_callbacks(app)

# -----------------------
# Expose for Gunicorn
# -----------------------
server = app.server

# -----------------------
# Local run
# -----------------------
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=10000)

