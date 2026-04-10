from dash.dependencies import Input, Output
from ui.pages.admin import admin_layout
from ui.pages.apartment import apartment_layout
from ui.pages.vendor import vendor_layout
from ui.pages.security import security_layout

def register_callbacks(app):

    @app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname')
    )
    def route(path):

        if path == "/admin":
            return admin_layout()

        elif path == "/apartment":
            return apartment_layout()

        elif path == "/vendor":
            return vendor_layout()

        elif path == "/security":
            return security_layout()

        return "Login Page (to be added)"