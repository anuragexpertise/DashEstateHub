from dash import html

def navbar():
    return html.Div([
        html.H2("EstateHub", style={"display": "inline-block"}),

        html.Div([
            html.A("Admin", href="/admin"),
            html.A("Apartment", href="/apartment"),
            html.A("Vendor", href="/vendor"),
            html.A("Security", href="/security"),
        ], style={"float": "right", "gap": "20px"})
    ], style={
        "padding": "15px",
        "background": "#111",
        "color": "white"
    })