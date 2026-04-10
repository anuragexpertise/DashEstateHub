from dash.dependencies import Input, Output, State
from flask import session

from services.auth_service import authenticate_user

from ui.pages.login import login_layout
from ui.pages.admin import admin_layout
from ui.pages.apartment import apartment_layout
from ui.pages.vendor import vendor_layout
from ui.pages.security import security_layout


def register_callbacks(app):

    # -----------------------
    # LOGIN ACTION
    # -----------------------
    @app.callback(
        Output("session", "data"),
        Output("login-output", "children"),
        Input("login-btn", "n_clicks"),
        State("login-email", "value"),
        State("login-password", "value"),
        prevent_initial_call=True
    )
    def login(n, email, password):

        user = authenticate_user(email, password)

        if not user:
            return None, "❌ Invalid credentials"

        session["user"] = user

        return user, "✅ Login successful"


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

        role = session_data["role"]

        if role == "admin":
            return admin_layout()

        elif role == "apartment":
            return apartment_layout()

        elif role == "vendor":
            return vendor_layout()

        elif role == "security":
            return security_layout()

        return login_layout()