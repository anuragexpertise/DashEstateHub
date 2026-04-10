from dash import html, dcc
from ui.components.navbar import navbar

def serve_layout():
    return html.Div([
        dcc.Location(id='url'),
        navbar(),
        html.Div(id='page-content')
    ])