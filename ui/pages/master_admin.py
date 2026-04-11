from dash import html, dcc

def layout():

    return html.Div([

        html.H2("🏢 Society Management"),

        # =========================
        # CREATE FORM
        # =========================
        html.Div([

            dcc.Input(id="soc-name", placeholder="Society Name"),
            dcc.Input(id="soc-email", placeholder="Society Email"),
            dcc.Input(id="soc-phone", placeholder="Phone"),

            dcc.Input(id="admin-email", placeholder="Admin Email"),
            dcc.Input(id="admin-password", placeholder="Admin Password", type="password"),

            html.Button("Create Society", id="create-soc-btn")

        ], style={"display": "grid", "gap": "10px", "maxWidth": "400px"}),

        html.Hr(),

        # =========================
        # LIST
        # =========================
        html.Div(id="society-list")

    ], style={"padding": "20px"})