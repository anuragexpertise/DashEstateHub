from dash import html, dcc

def login_layout():

    return html.Div([

        # Background overlay
        html.Div(style={
            "position": "fixed",
            "top": "0",
            "left": "0",
            "width": "100%",
            "height": "100%",
            "backgroundImage": "url('/assets/estate_management_light.jpg')",
            "backgroundSize": "cover",
            "backgroundPosition": "center",
            "filter": "brightness(0.7)",
            "zIndex": "-1"
        }),

        # Center Glass Card
        html.Div([

            html.H2("EstateHub Login", style={
                "textAlign": "center",
                "marginBottom": "20px",
                "color": "#fff"
            }),

            dcc.Input(
                id="login-email",
                type="email",
                placeholder="Email",
                style=INPUT_STYLE
            ),

            dcc.Input(
                id="login-password",
                type="password",
                placeholder="Password",
                style=INPUT_STYLE
            ),

            html.Button(
                "Login",
                id="login-btn",
                style=BUTTON_STYLE
            )

        ], style=GLASS_CARD_STYLE)

    ])
GLASS_CARD_STYLE = {
    "width": "350px",
    "margin": "auto",
    "marginTop": "10%",
    "padding": "30px",

    "borderRadius": "15px",

    "background": "rgba(255, 255, 255, 0.1)",
    "backdropFilter": "blur(15px)",
    "WebkitBackdropFilter": "blur(15px)",

    "border": "1px solid rgba(255,255,255,0.2)",

    "boxShadow": "0 8px 32px rgba(0,0,0,0.3)"
}

INPUT_STYLE = {
    "width": "100%",
    "padding": "12px",
    "marginBottom": "15px",
    "borderRadius": "8px",
    "border": "none",
    "outline": "none"
}

BUTTON_STYLE = {
    "width": "100%",
    "padding": "12px",
    "background": "#00c851",
    "color": "white",
    "border": "none",
    "borderRadius": "8px",
    "fontWeight": "bold",
    "cursor": "pointer"
}