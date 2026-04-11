from dash import html, dcc

layout = html.Div([
    html.H2("Create Society"),

    dcc.Input(id="soc-name", placeholder="Society Name"),
    dcc.Input(id="soc-email", placeholder="Email"),
    dcc.Input(id="soc-phone", placeholder="Phone"),
    dcc.Input(id="soc-address", placeholder="Address"),

    dcc.Input(id="soc-sec-name", placeholder="Secretary Name"),
    dcc.Input(id="soc-sec-phone", placeholder="Secretary Phone"),

    dcc.DatePickerSingle(id="soc-plan-validity"),
    dcc.DatePickerSingle(id="soc-arrear-date"),

    html.Button("Create Society", id="create-society-btn"),

    html.Div(id="society-output")
])