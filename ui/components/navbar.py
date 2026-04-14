from dash import html, dcc

def get_navbar(session):

    if not session:
        return ""

    role = session.get("role")
    society_id = session.get("society_id")

    links = []

    # MASTER ADMIN
    if role == "admin" and society_id == 0:
        links += [
            dcc.Link("Dashboard", href="/master", className="nav-item"),
            dcc.Link("Societies", href="/create-society", className="nav-item"),
        ]

    elif role == "admin":
        links += [
            dcc.Link("Dashboard", href="/admin", className="nav-item"),
            dcc.Link("Apartments", href="/apartments", className="nav-item"),
            dcc.Link("Vendors", href="/vendors", className="nav-item"),
            dcc.Link("Accounts", href="/accounts", className="nav-item"),
        ]

    elif role == "security":
        links += [
            dcc.Link("Scan", href="/security", className="nav-item"),
            dcc.Link("Attendance", href="/attendance", className="nav-item"),
        ]

    elif role == "vendor":
        links += [
            dcc.Link("Dashboard", href="/vendor", className="nav-item"),
        ]

    elif role == "apartment":
        links += [
            dcc.Link("My Dues", href="/apartment", className="nav-item"),
        ]

    links.append(html.Button(
        "Logout",
        id="logout-btn",
        style={
            "padding": "8px 16px",
            "backgroundColor": "rgba(220, 53, 69, 0.8)",
            "color": "white",
            "border": "none",
            "borderRadius": "5px",
            "cursor": "pointer"
        }
    ))

    return html.Div(
        links,
        style={
            "display": "flex",
            "gap": "20px",
            "padding": "15px 30px",
            "background": "rgba(0,0,0,0.6)",
            "backdropFilter": "blur(10px)",
            "color": "white",
            "borderRadius": "10px",
            "marginBottom": "10px"
        }
    )