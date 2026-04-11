from dash import Input, Output, State, html
from services.auth_service import authenticate_user
from services.dashboard_service import get_dashboard_metrics

from ui.pages.login import login_layout
from ui.pages.admin import admin_layout_dynamic
from ui.pages.master_admin import layout as master_layout
from ui.pages.apartment import apartment_layout
from ui.pages.vendor import vendor_layout
from ui.pages.security import security_layout


def register_auth_callbacks(app):

    # =========================================
    # LOGIN CALLBACK (ONLY login-btn used)
    # =========================================
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

        if not email or not password:
            return None, "/", {
                "type": "error",
                "message": "Enter email and password"
            }

        user = authenticate_user(email, password)

        if not user:
            return None, "/", {
                "type": "error",
                "message": "Invalid credentials"
            }

        # ✅ MASTER ADMIN (id = 0)
        if user["user_id"] == 0:
            return user, "/master", {
                "type": "success",
                "message": "Master Admin Login"
            }

        # ✅ ROLE-BASED ROUTING
        role = user["role"]

        if role == "admin":
            return user, "/admin", {"type": "success", "message": "Login successful"}

        if role == "apartment":
            return user, "/apartment", {"type": "success", "message": "Login successful"}

        if role == "vendor":
            return user, "/vendor", {"type": "success", "message": "Login successful"}

        if role == "security":
            return user, "/security", {"type": "success", "message": "Login successful"}

        return None, "/", {
            "type": "error",
            "message": "Unknown role"
        }

    # =========================================
    # LOGOUT CALLBACK (ONLY logout-btn used)
    # =========================================
    @app.callback(
        Output("session", "data", allow_duplicate=True),
        Output("url", "pathname", allow_duplicate=True),
        Output("toast-store", "data", allow_duplicate=True),
        Input("logout-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def logout_handler(n):

        return None, "/", {
            "type": "success",
            "message": "Logged out successfully"
        }

    # =========================================
    # ROUTER (NO duplicate outputs used elsewhere)
    # =========================================
    @app.callback(
        Output("page-content", "children"),
        Input("url", "pathname"),
        Input("session", "data")
    )
    def route(pathname, session_data):

        print("PATH:", pathname)
        print("SESSION:", session_data)

        # 🔴 NOT LOGGED IN
        if not session_data or "role" not in session_data:
            return login_layout()

        role = session_data.get("role")
        user_id = session_data.get("user_id")
        society_id = session_data.get("society_id")

        # 🟢 MASTER ADMIN
        if pathname == "/master":
            if user_id == 0:
                return master_layout()
            return "❌ Unauthorized"

        # 🟢 SOCIETY ADMIN
        if pathname == "/admin":
            if role == "admin" and user_id != 0:
                try:
                    data = get_dashboard_metrics(society_id)
                    return admin_layout_dynamic(data)
                except Exception as e:
                    return html.Div(f"Dashboard Error: {str(e)}")
            return "❌ Unauthorized"

        # 🟢 OTHER ROLES
        if pathname == "/apartment":
            return apartment_layout() if role == "apartment" else "❌ Unauthorized"

        if pathname == "/vendor":
            return vendor_layout() if role == "vendor" else "❌ Unauthorized"

        if pathname == "/security":
            return security_layout() if role == "security" else "❌ Unauthorized"

        # 🔁 DEFAULT
        return login_layout()