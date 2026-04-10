from dash import html

def kpi_card(title, value):
    return html.Div([
        html.H4(title),
        html.H2(value)
    ], style={
        "padding": "20px",
        "background": "#1e1e1e",
        "color": "white",
        "borderRadius": "10px",
        "width": "22%",
        "display": "inline-block",
        "margin": "1%"
    })