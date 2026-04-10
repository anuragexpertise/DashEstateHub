from flask import Flask
from dash import Dash
from ui.layout import create_layout
from ui.callbacks import register_callbacks

server = Flask(__name__)

app = Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True
)

# ✅ Attach layout
app.layout = create_layout()

# ✅ Register callbacks
register_callbacks(app)

# expose server
server = app.server

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=10000)