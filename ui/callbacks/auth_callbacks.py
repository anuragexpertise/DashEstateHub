from dash.dependencies import Input, Output, State
from flask import session

from services.auth_service import authenticate_user

from ui.pages.login import login_layout
from ui.pages.admin import admin_layout
from ui.pages.apartment import apartment_layout
from ui.pages.vendor import vendor_layout
from ui.pages.security import security_layout
from dash.exceptions import PreventUpdate
from flask import session

def register_auth_callbacks(app):

    # -----------------------
    # LOGIN ACTION
    # -----------------------
    @app.callback(
        Output("session", "data"),
        Output("url", "pathname"),   # 👈 redirect
        Output("login-output", "children"),
        Input("login-btn", "n_clicks"),
        State("login-email", "value"),
        State("login-password", "value"),
        prevent_initial_call=True
    )
    def login(n, email, password):

        user = authenticate_user(email, password)

        if not user:
            return None, "/", "❌ Invalid credentials"

        session["user"] = user

        # redirect based on role
        role = user["role"]

        if role == "admin":
            return user, "/admin", "✅ Login successful"

        if role == "apartment":
            return user, "/apartment", "✅ Login successful"

        if role == "vendor":
            return user, "/vendor", "✅ Login successful"

        if role == "security":
            return user, "/security", "✅ Login successful"

        return user, "/", "✅ Login"
    
    @app.callback(
        Output("session", "data"),
        Output("url", "pathname"),
        Input("logout-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def logout(n):

        from flask import session
        session.clear()

        return None, "/"

    # -----------------------
    # ROUTING
    # -----------------------
    @app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname'),
        Input('session', 'data')
    )
    def route(path, session_data):

        # 🔴 ALWAYS handle None path
        if not path:
            path = "/"

        # 🔴 If NOT logged in → show login ALWAYS
        if not session_data:
            return login_layout()

        role = session_data.get("role")

        # 🔴 ROLE PROTECTION
        if path == "/admin":
            if role != "admin":
                return "❌ Unauthorized"
            return admin_layout()

        elif path == "/apartment":
            if role != "apartment":
                return "❌ Unauthorized"
            return apartment_layout()

        elif path == "/vendor":
            if role != "vendor":
                return "❌ Unauthorized"
            return vendor_layout()

        elif path == "/security":
            if role != "security":
                return "❌ Unauthorized"
            return security_layout()

        # 🔴 DEFAULT (IMPORTANT)
        return login_layout()