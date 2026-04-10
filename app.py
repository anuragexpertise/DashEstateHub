from flask import Flask
from dash import Dash
from dash import html


server = Flask(__name__)

app = Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True
)


app.layout = html.Div([
    html.H1("EstateHub Running ✅")
])

# expose Flask server for Gunicorn
server = app.server
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=10000)