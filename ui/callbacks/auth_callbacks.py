from dash import Input, Output, State
from flask import session

from services.auth_service import authenticate_user

# Page layouts
from ui.pages.login import login_layout
from ui.pages.admin import admin_layout
from ui.pages.apartment import apartment_layout
from ui.pages.vendor import vendor_layout
from ui.pages.security import security_layout
from ui.pages.master_admin import layout as master_admin_layout


def register_auth_callbacks(app):

    # =========================================================
    # 🔐 LOGIN HANDLER (ONLY PLACE THAT SETS TOAST)
    # =========================================================
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

        if not n_clicks:
            return None, "/", None

        user = authenticate_user(email, password)

        # ❌ INVALID LOGIN
        if not user:
            return None, "/", {
                "type": "error",
                "message": "Invalid credentials"
            }

        # ✅ STORE SESSION
        session["user"] = user

        role = user.get("role")
        society_id = user.get("society_id")

        # 🟢 MASTER ADMIN
        if role == "admin" and society_id == 0:
            return user, "/master", {
                "type": "success",
                "message": "Master Admin login successful"
            }

        # 🟢 ROLE ROUTING
        if role == "admin":
            return user, "/admin", {
                "type": "success",
                "message": "Login successful"
            }

        if role == "apartment":
            return user, "/apartment", {
                "type": "success",
                "message": "Login successful"
            }

        if role == "vendor":
            return user, "/vendor", {
                "type": "success",
                "message": "Login successful"
            }

        if role == "security":
            return user, "/security", {
                "type": "success",
                "message": "Login successful"
            }

        # fallback
        return None, "/", {
            "type": "error",
            "message": "Unauthorized role"
        }

    # =========================================================
    # 🌐 ROUTING + LOGOUT (NO TOAST HERE → avoids duplication)
    # =========================================================
    @app.callback(
        Output("page-content", "children"),
        Input("url", "pathname"),
        Input("session", "data")
    )
    def route_handler(pathname, session_data):

        # 🔴 LOGOUT
        if pathname == "/logout":
            session.clear()
            return login_layout()

        # 🔴 NOT LOGGED IN
        if not session_data:
            return login_layout()

        role = session_data.get("role")
        society_id = session_data.get("society_id")

        # 🟢 MASTER ADMIN
        if pathname == "/master":
            if role == "admin" and society_id == 0:
                return master_admin_layout
            return "❌ Unauthorized"

        # 🟢 ADMIN
        if pathname == "/admin":
            if role == "admin":
                return admin_layout()
            return "❌ Unauthorized"

        # 🟢 APARTMENT
        if pathname == "/apartment":
            if role == "apartment":
                return apartment_layout()
            return "❌ Unauthorized"

        # 🟢 VENDOR
        if pathname == "/vendor":
            if role == "vendor":
                return vendor_layout()
            return "❌ Unauthorized"

        # 🟢 SECURITY
        if pathname == "/security":
            if role == "security":
                return security_layout()
            return "❌ Unauthorized"

        # 🟡 DEFAULT
        return login_layout()