from flask import Flask
from dash import Dash, html, dcc

# from ui.layout import serve_layout
# from ui.callbacks import register_callbacks

server = Flask(__name__)

app = Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True
)

server = app.server

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)