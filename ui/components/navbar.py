from dash import html, dcc

def navbar():
    return html.Div([
        dcc.Link("Admin", href="/admin"),
        " | ",
        dcc.Link("Apartment", href="/apartment"),
        " | ",
        dcc.Link("Vendor", href="/vendor"),
        " | ",
        dcc.Link("Security", href="/security"),
    ], style={"padding": "20px", "background": "#eee"})