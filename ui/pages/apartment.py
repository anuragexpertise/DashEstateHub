from dash import html

def apartment_layout():
    return html.Div([

        html.H3("Apartment Dashboard"),

        html.Div([
            html.H4("QR Code"),
            html.Div(id="qr-display")
        ]),

        html.H4("Ledger"),
        html.Div(id="apartment-ledger"),

        html.H4("Dues"),
        html.Div(id="apartment-dues")

    ], style={"padding": "20px"})