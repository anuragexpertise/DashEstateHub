from dash import html

def vendor_layout():
    return html.Div([

        html.H3("Vendor Dashboard"),

        html.H4("QR Code"),
        html.Div(id="vendor-qr"),

        html.H4("Buy Pass"),
        html.Button("1 Day"),
        html.Button("7 Day"),
        html.Button("1 Month"),

        html.H4("Payment History"),
        html.Div(id="vendor-payments")

    ], style={"padding": "20px"})