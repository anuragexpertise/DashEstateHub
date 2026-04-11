from dash import html, dcc

def serve_layout():
    return html.Div([

        dcc.Location(id="url"),
        dcc.Store(id="session"),
        dcc.Store(id="toast-store"),

        # Toast container
        html.Div(id="toast-container", style={
            "position": "fixed",
            "top": "20px",
            "right": "20px",
            "zIndex": "9999"
        }),

        html.Div(id="navbar"),
        html.Div(id="page-content")

    ],
    # ✅ APPLY GLOBAL STYLE HERE (OUTERMOST DIV)
    style={
        "fontFamily": "Segoe UI",
        "backgroundColor": "#f5f7fa",
        "minHeight": "100vh"
    })