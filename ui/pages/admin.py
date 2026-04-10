from dash import html, dcc
from ui.components.kpi_cards import kpi_card

def admin_layout():
    return html.Div([

        html.H2("Admin Dashboard"),

        html.Div([
            kpi_card("Total Revenue", "₹0"),
            kpi_card("Pending Dues", "₹0"),
            kpi_card("Vendors", "0"),
            kpi_card("Security Staff", "0"),
        ]),

        dcc.Tabs([

            dcc.Tab(label="Cashbook", children=[
                html.Div(id="cashbook-table")
            ]),

            dcc.Tab(label="Ledger", children=[
                html.Div(id="ledger-table")
            ]),

            dcc.Tab(label="Accounts", children=[
                html.Div(id="accounts-table")
            ]),

            dcc.Tab(label="Charges & Fines", children=[
                html.Div(id="charges-table")
            ]),

            dcc.Tab(label="Settings", children=[
                html.Div("Society Settings Here")
            ])

        ])
    ], style={"padding": "20px"})