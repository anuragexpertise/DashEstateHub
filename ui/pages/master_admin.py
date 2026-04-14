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
            dcc.Input(id="soc-address", placeholder="Address"),
            dcc.Input(id="soc-sec-name", placeholder="Secretary Name"),
            dcc.Input(id="soc-sec-phone", placeholder="Secretary Phone"),
            dcc.DatePickerSingle(id="soc-plan-validity", placeholder="Plan Validity"),
            dcc.DatePickerSingle(id="soc-arrear-date", placeholder="Arrear Start Date"),

            dcc.Input(id="admin-email", placeholder="Admin Email"),
            dcc.Input(id="admin-password", placeholder="Admin Password", type="password"),

            html.Button("Create Society", id="create-society-btn")

        ], style={"display": "grid", "gap": "10px", "maxWidth": "400px"}),

        html.Hr(),

        # =========================
        # LIST
        # =========================
        html.Div(id="society-list")

    ], style={"padding": "20px"})