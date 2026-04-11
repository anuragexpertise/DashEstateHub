from dash import html

def get_navbar(session):
    if not session:
        return ""

    role = session.get("role")
    society_id = session.get("society_id")

    links = [
        html.A("Dashboard", href="/dashboard", style={"marginRight": "20px"})
    ]

    # ✅ MASTER ADMIN (society_id = 0)
    if society_id == 0:
        links += [
            html.A("Create Society", href="/create-society", style={"marginRight": "20px"}),
            html.A("Manage Societies", href="/manage-societies", style={"marginRight": "20px"})
        ]

    # ✅ NORMAL ADMIN
    if role == "admin" and society_id != 0:
        links += [
            html.A("Apartments", href="/apartments", style={"marginRight": "20px"}),
            html.A("Vendors", href="/vendors", style={"marginRight": "20px"}),
            html.A("Accounts", href="/accounts", style={"marginRight": "20px"})
        ]

    links.append(html.A("Logout", href="/logout"))

    return html.Div(
        links,
        style={
            "background": "#111",
            "padding": "15px",
            "color": "white"
        }
    )