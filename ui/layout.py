from dash import html, dcc

def serve_layout():
    return html.Div([

        dcc.Location(id="url"),
        dcc.Store(id="session", storage_type="session"),
        dcc.Store(id="toast-store"),

        # Toast
        html.Div(id="toast-container", style={
            "position": "fixed",
            "top": "20px",
            "right": "20px",
            "zIndex": "9999"
        }),

        # Navbar
        html.Div(id="navbar"),

        # Page content
        html.Div(id="page-content")

    ],
    style={
        "fontFamily": "Segoe UI, sans-serif",
        "minHeight": "100vh"
    })