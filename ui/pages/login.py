from dash import html, dcc


def login_layout():
    """Basic login page - now only used for direct login"""
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


def society_login_layout(society_name="EstateHub", society_logo=None, society_background=None, saved_email=None, default_method="password"):
    """
    Society-specific login page - Second step in two-stage login.
    Shows society logo and background, with tabbed login methods.
    
    Args:
        society_name: Name of the society
        society_logo: URL to society logo image
        society_background: URL to society background image
    
    Returns:
        Dash layout component
    """
    
    # Use default background if none provided
    bg_image = society_background or "/assets/estate_management_light.jpg"
    
    return html.Div([
        # Background overlay
        html.Div(style={
            "position": "fixed",
            "top": "0",
            "left": "0",
            "width": "100%",
            "height": "100%",
            "backgroundImage": f"url('{bg_image}')",
            "backgroundSize": "cover",
            "backgroundPosition": "center",
            "filter": "brightness(0.6)",
            "zIndex": "-1"
        }),

        html.Div([
            # Society logo (if available)
            html.Div([
                html.Img(
                    src=society_logo,
                    className="society-logo",
                    style={"maxHeight": "60px", "marginBottom": "16px"}
                ) if society_logo else "",
                html.H2(f"{society_name} Login", className="login-title")
            ], className="society-login-header"),

            # Tabbed login interface
            dcc.Tabs(
                id="login-method-tabs",
                value=default_method,
                children=[
                    # ========================
                    # PASSWORD TAB
                    # ========================
                    dcc.Tab(
                        label="Password",
                        value="password",
                        children=[
                            html.Div([
                                dcc.Input(
                                    id="login-email",
                                    type="email",
                                    placeholder="Email",
                                    value=saved_email,
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
                                ),
                                html.Div([
                                    dcc.Link("Forgot Password?", href="/forgot-password", 
                                           style={"color": "rgba(255,255,255,0.8)", "fontSize": "0.9rem"})
                                ], style={"marginTop": "15px", "textAlign": "center"})
                            ], className="login-form-tab")
                        ]
                    ),
                    
                    # ========================
                    # PIN TAB
                    # ========================
                    dcc.Tab(
                        label="PIN",
                        value="pin",
                        children=[
                            html.Div([
                                dcc.Input(
                                    id="login-email-pin",
                                    type="email",
                                    placeholder="Email",
                                    value=saved_email,
                                    style=INPUT_STYLE
                                ),
                                dcc.Input(
                                    id="login-pin",
                                    type="password",
                                    placeholder="4-Digit PIN",
                                    style=INPUT_STYLE
                                ),
                                html.Button(
                                    "Login with PIN",
                                    id="login-pin-btn",
                                    style=BUTTON_STYLE
                                ),
                                html.Div([
                                    dcc.Link("Forgot PIN?", href="/forgot-pin", 
                                           style={"color": "rgba(255,255,255,0.8)", "fontSize": "0.9rem"})
                                ], style={"marginTop": "15px", "textAlign": "center"})
                            ], className="login-form-tab")
                        ]
                    ),
                    
                    # ========================
                    # PATTERN TAB
                    # ========================
                    dcc.Tab(
                        label="Pattern",
                        value="pattern",
                        children=[
                            html.Div([
                                dcc.Input(
                                    id="login-email-pattern",
                                    type="email",
                                    placeholder="Email",
                                    value=saved_email,
                                    style=INPUT_STYLE
                                ),
                                dcc.Input(
                                    id="login-pattern",
                                    type="text",
                                    placeholder="9-Dot Pattern (e.g., 1-2-3-5-7)",
                                    style=INPUT_STYLE
                                ),
                                html.Button(
                                    "Login with Pattern",
                                    id="login-pattern-btn",
                                    style=BUTTON_STYLE
                                ),
                                html.Div([
                                    dcc.Link("Forgot Pattern?", href="/forgot-pattern", 
                                           style={"color": "rgba(255,255,255,0.8)", "fontSize": "0.9rem"})
                                ], style={"marginTop": "15px", "textAlign": "center"})
                            ], className="login-form-tab")
                        ]
                    )
                ],
                style=TABS_STYLE
            ),

            # Remember Me checkbox
            html.Div([
                html.Label([
                    dcc.Checklist(
                        id="remember-me-checkbox",
                        options=[{"label": " Remember me on this device", "value": 1}],
                        value=[],
                        style={"display": "inline-block"}
                    )
                ], style={"color": "rgba(255,255,255,0.8)", "fontSize": "0.9rem", "marginTop": "20px"})
            ]),

            # Change Society button
            html.Div([
                dcc.Link("← Change Society", href="/", 
                       style={"color": "rgba(255,255,255,0.7)", "fontSize": "0.85rem", "marginTop": "20px", "display": "block", "textAlign": "center"})
            ])

        ], style=GLASS_CARD_STYLE)
    ])


GLASS_CARD_STYLE = {
    "width": "380px",
    "margin": "auto",
    "marginTop": "8%",
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
    "marginTop": "10px",
    "marginBottom": "15px",
    "borderRadius": "8px",
    "border": "none",
    "backgroundColor": "rgba(52, 211, 153, 0.9)",
    "color": "#fff",
    "fontSize": "1rem",
    "fontWeight": "600",
    "cursor": "pointer",
    "transition": "all 0.3s ease"
}

TABS_STYLE = {
    "marginTop": "20px",
    "marginBottom": "20px"
}