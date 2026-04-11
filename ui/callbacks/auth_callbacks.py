from dash import Input, Output, State
from dash import html

from services.auth_service import authenticate_user
from services.dashboard_service import get_dashboard_metrics

# Pages
from ui.pages.login import login_layout
from ui.pages.admin import admin_layout_dynamic
from ui.pages.apartment import apartment_layout
from ui.pages.vendor import vendor_layout
from ui.pages.security import security_layout
from ui.pages.master_admin import layout as master_admin_layout


def register_auth_callbacks(app):

    # ===================================
    # LOGIN HANDLER
    # ===================================
    @app.callback(
        Output("session", "data"),
        Output("url", "pathname"),
        Output("toast-store", "data"),
        Input("login-btn", "n_clicks"),
        State("login-email", "value"),
        State("login-password", "value"),
        prevent_initial_call=True
    )
    def login_handler(n_clicks, email, password):

        user = authenticate_user(email, password)

        if not user:
            return None, "/", {
                "type": "error",
                "message": "Invalid credentials"
            }

        role = user["role"]
        society_id = user["society_id"]

        # MASTER ADMIN
        if role == "admin" and society_id == 0:
            return user, "/master", {
                "type": "success",
                "message": "Master Admin login"
            }

        # ADMIN
        if role == "admin":
            return user, "/admin", {
                "type": "success",
                "message": "Login successful"
            }

        # OTHER ROLES
        if role == "apartment":
            return user, "/apartment", {"type": "success", "message": "Welcome"}

        if role == "vendor":
            return user, "/vendor", {"type": "success", "message": "Welcome"}

        if role == "security":
            return user, "/security", {"type": "success", "message": "Welcome"}

        return None, "/", {"type": "error", "message": "Unauthorized"}

    # ===================================
    # ROUTER (ONLY ONE OWNER)
    # ===================================
    @app.callback(
        Output("page-content", "children"),
        Input("url", "pathname"),
        Input("session", "data")
    )
    def route_handler(pathname, session_data):

        print("PATH:", pathname)
        print("SESSION:", session_data)

        # LOGOUT
        if pathname == "/logout":
            return login_layout()

        # NOT LOGGED IN
        if not session_data:
            return login_layout()

        role = session_data.get("role")
        society_id = session_data.get("society_id")

        # MASTER ADMIN
        if pathname == "/master":
            if role == "admin" and society_id == 0:
                return master_admin_layout
            return "❌ Unauthorized"

        # ADMIN DASHBOARD
        if pathname == "/admin":
            if role == "admin":
                try:
                    data = get_dashboard_metrics(society_id)
                    return admin_layout_dynamic(data)
                except Exception as e:
                    print("DASHBOARD ERROR:", e)

                    # 🔴 FALLBACK UI (prevents white screen)
                    return html.Div([
                        html.H3("Dashboard Error"),
                        html.Div(str(e))
                    ])
            return "❌ Unauthorized"

        # OTHER ROLES
        if pathname == "/apartment":
            return apartment_layout()

        if pathname == "/vendor":
            return vendor_layout()

        if pathname == "/security":
            return security_layout()

        return login_layout()