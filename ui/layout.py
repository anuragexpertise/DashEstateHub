from dash import html, dcc
from ui.components.navbar import navbar

def serve_layout():
    return html.Div([

        dcc.Location(id='url'),

        # 🔴 SESSION STORAGE
        dcc.Store(id='session', storage_type='session', data=None),

        navbar(),

        html.Div(id='page-content')
    ])