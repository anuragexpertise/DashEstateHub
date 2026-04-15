from dash import html, dcc

def serve_layout():
    return html.Div([

        dcc.Location(id="url"),
        dcc.Store(id="session", storage_type="memory"),
        dcc.Store(id="toast-store"),
        dcc.Store(id="cookie-store", storage_type="local"),  # Persistent cookie storage
        dcc.Store(id="dummy", data="init"),  # Dummy store to trigger initial callback

        # Toast
        html.Div(id="toast-container", style={
            "position": "fixed",
            "top": "20px",
            "right": "20px",
            "zIndex": "9999"
        }),

        # Navbar (hidden during login)
        html.Div(id="navbar"),

        # Page content
        html.Div(id="page-content")

    ],
    style={
        "fontFamily": "Segoe UI, sans-serif",
        "minHeight": "100vh"
    })