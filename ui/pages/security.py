from dash import html, dcc

def security_layout():
    return html.Div([

        html.H2("Security Scanner"),

        dcc.Input(
            id="qr-input",
            placeholder="Scan QR Code",
            style={"width": "300px", "height": "40px"}
        ),

        html.Button("Scan", id="scan-btn"),

        html.Div(id="scan-result", style={
            "fontSize": "40px",
            "marginTop": "20px"
        })

    ], style={"padding": "50px", "textAlign": "center"})