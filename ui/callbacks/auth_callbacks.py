from dash import ctx
from dash.dependencies import Input, Output, State
from flask import session

from services.auth_service import authenticate_user
from ui.pages.login import login_layout
from ui.pages.admin import admin_layout
from ui.pages.apartment import apartment_layout
from ui.pages.vendor import vendor_layout
from ui.pages.security import security_layout


def register_auth_callbacks(app):

    # -----------------------
    # AUTH HANDLER (LOGIN + LOGOUT)
    # -----------------------
    @app.callback(
        Output("session", "data"),
        Output("url", "pathname"),
        Output("login-output", "children"),
        Input("login-btn", "n_clicks"),
        Input("logout-btn", "n_clicks"),
        State("login-email", "value"),
        State("login-password", "value"),
        prevent_initial_call=True
    )
    def auth_handler(login_click, logout_click, email, password):

        trigger = ctx.triggered_id

        # 🔴 LOGOUT
        if trigger == "logout-btn":
            session.clear()
            return None, "/", ""

        # 🔴 LOGIN
        if trigger == "login-btn":
            user = authenticate_user(email, password)

            if not user:
                return None, "/", "❌ Invalid credentials"

            session["user"] = user

            role = user["role"]

            if role == "admin":
                return user, "/admin", "✅ Login"

            if role == "apartment":
                return user, "/apartment", "✅ Login"

            if role == "vendor":
                return user, "/vendor", "✅ Login"

            if role == "security":
                return user, "/security", "✅ Login"

        return None, "/", ""


    # -----------------------
    # ROUTING
    # -----------------------
    @app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname'),
        Input('session', 'data')
    )
    def route(path, session_data):

        if not session_data:
            return login_layout()

        role = session_data.get("role")

        if path == "/admin":
            return admin_layout() if role == "admin" else "❌ Unauthorized"

        if path == "/apartment":
            return apartment_layout() if role == "apartment" else "❌ Unauthorized"

        if path == "/vendor":
            return vendor_layout() if role == "vendor" else "❌ Unauthorized"

        if path == "/security":
            return security_layout() if role == "security" else "❌ Unauthorized"

        return login_layout()