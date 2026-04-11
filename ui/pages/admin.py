from dash import html, dcc

# ======================
# STYLES
# ======================
ROW_STYLE = {
    "display": "flex",
    "gap": "20px",
    "marginBottom": "20px",
    "flexWrap": "wrap"
}

CARD_STYLE = {
    "flex": "1",
    "minWidth": "200px",
    "padding": "20px",
    "borderRadius": "12px",
    "background": "rgba(255,255,255,0.15)",
    "backdropFilter": "blur(10px)",
    "boxShadow": "0 4px 20px rgba(0,0,0,0.2)"
}

PANEL_STYLE = {
    "flex": "1",
    "padding": "20px",
    "borderRadius": "12px",
    "background": "rgba(255,255,255,0.1)",
    "backdropFilter": "blur(8px)"
}

# ======================
# COMPONENTS
# ======================
def kpi_card(title, value):
    return html.Div([
        html.H4(title),
        html.H2(value)
    ], style=CARD_STYLE)


def action_card(title, link):
    return dcc.Link(
        html.Div(title, style=CARD_STYLE),
        href=link
    )

# ======================
# STATIC FALLBACK (SAFE)
# ======================
def admin_layout():
    return html.Div("Loading Dashboard...", style={"padding": "20px"})


# ======================
# DYNAMIC DASHBOARD
# ======================
def admin_layout_dynamic(data):

    return html.Div([

        # HEADER
        html.H2("Admin Dashboard", style={"marginBottom": "20px"}),

        # KPI ROW
        html.Div([
            kpi_card("Total Dues", f"₹ {data.get('dues', 0)}"),
            kpi_card("Collected", f"₹ {data.get('collected', 0)}"),
            kpi_card("Active Vendors", data.get("vendors", 0)),
            kpi_card("Gate Entries Today", data.get("entries", 0)),
        ], style=ROW_STYLE),

        # ACTIONS
        html.Div([
            action_card("➕ Add Apartment", "/apartments"),
            action_card("🏢 Manage Society", "/create-society"),
            action_card("💰 Charges & Fines", "/charges"),
            action_card("📊 Accounts", "/accounts"),
        ], style=ROW_STYLE),

        # PANELS
        html.Div([

            html.Div([
                html.H4("🚪 Gate Activity"),
                html.Div("No recent entries")
            ], style=PANEL_STYLE),

            html.Div([
                html.H4("💳 Recent Payments"),
                html.Div("No recent payments")
            ], style=PANEL_STYLE),

        ], style=ROW_STYLE)

    ], style={"padding": "20px"})