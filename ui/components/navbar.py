from dash import html

def get_navbar(session):

    if not session:
        return ""

    role = session.get("role")
    society_id = session.get("society_id")

    links = []

    # MASTER ADMIN
    if role == "admin" and society_id == 0:
        links += [
            html.A("Dashboard", href="/master"),
            html.A("Societies", href="/create-society"),
        ]

    elif role == "admin":
        links += [
            html.A("Dashboard", href="/admin"),
            html.A("Apartments", href="/apartments"),
            html.A("Vendors", href="/vendors"),
            html.A("Accounts", href="/accounts"),
        ]

    elif role == "security":
        links += [
            html.A("Scan", href="/security"),
            html.A("Attendance", href="/attendance"),
        ]

    elif role == "vendor":
        links += [
            html.A("Dashboard", href="/vendor"),
        ]

    elif role == "apartment":
        links += [
            html.A("My Dues", href="/apartment"),
        ]

    links.append(html.A("Logout", href="/logout"))

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