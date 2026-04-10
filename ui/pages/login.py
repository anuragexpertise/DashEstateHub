from dash import html, dcc

def login_layout():
    return html.Div([
        html.H2("Login"),

        dcc.Input(id="login-email", placeholder="Email", type="email"),
        dcc.Input(id="login-password", placeholder="Password", type="password"),

        html.Button("Login", id="login-btn"),

        html.Div(id="login-output")
    ])