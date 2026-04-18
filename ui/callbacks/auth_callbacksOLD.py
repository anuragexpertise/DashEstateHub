from dash import Input, Output, State, html, dcc
import dash
from services.auth_service import (
    authenticate_user,
    authenticate_pin, 
    authenticate_pattern
)
from services.society_service import get_societies, get_society_details
from services.dashboard_service import get_dashboard_metrics

from ui.pages.login import login_layout, society_login_layout
from ui.pages.society_select import society_select_layout
from ui.pages.admin import admin_layout_dynamic
from ui.pages.master_admin import layout as master_layout
from ui.pages.apartment import apartment_layout
from ui.pages.vendor import vendor_layout
from ui.pages.security import security_layout


def register_auth_callbacks(app):
    # =========================================
    # SOCIETY SELECTION CALLBACK
    # =========================================
    @app.callback(
        Output("session", "data"),
        Output("url", "pathname"),
        Output("toast-store", "data"),
        Input("society-select-btn", "n_clicks"),
        State("society-dropdown", "value"),
        prevent_initial_call=True
    )
    def select_society(n_clicks, society_id):
        """
        Handle society selection from first login page.
        Sets session with society_id and redirects to society login.
        """
        if not society_id:
            return dash.no_update, dash.no_update, {
                "type": "error",
                "message": "Please select a society"
            }

        # Store society selection in session (without user being logged in yet)
        session_data = {
            "society_id": society_id,
            "authenticated": False
        }

        return session_data, "/login", {
            "type": "success",
            "message": "Society selected. Please log in."
        }

    # =========================================
    # SOCIETY LOGIN - PASSWORD METHOD
    # =========================================
    @app.callback(
        Output("session", "data", allow_duplicate=True),
        Output("url", "pathname", allow_duplicate=True),
        Output("toast-store", "data", allow_duplicate=True),
        Output("cookie-store", "data", allow_duplicate=True),
        Input("login-btn", "n_clicks"),
        State("login-email", "value"),
        State("login-password", "value"),
        State("session", "data"),
        State("remember-me-checkbox", "value"),
        prevent_initial_call=True
    )
    def password_login(n_clicks, email, password, session_data, remember):
        """Authenticate with email/password method."""
        if not email or not password:
            return dash.no_update, dash.no_update, {
                "type": "error",
                "message": "Enter email and password"
            }, dash.no_update

        society_id = session_data.get("society_id") if session_data else None
        user = authenticate_user(email, password, society_id)

        if not user:
            return dash.no_update, dash.no_update, {
                "type": "error",
                "message": "Invalid email or password"
            }, dash.no_update

        # Successful login - set full session
        user["authenticated"] = True
        
        # Store preferences in local cookie-store
        cookie_data = {"email": email, "society_id": society_id, "method": "pattern"} if remember else dash.no_update

        if user.get("role") == "admin" and user.get("society_id") is None:
            return user, "/master", {"type": "success", "message": "Master Admin Login"}, cookie_data

        role = user["role"]
        if role == "admin":
            return user, "/admin", {"type": "success", "message": "Login successful"}, cookie_data
        if role == "apartment":
            return user, "/apartment", {"type": "success", "message": "Login successful"}, cookie_data
        if role == "vendor":
            return user, "/vendor", {"type": "success", "message": "Login successful"}, cookie_data
        if role == "security":
            return user, "/security", {"type": "success", "message": "Login successful"}, cookie_data

        return dash.no_update, dash.no_update, {
            "type": "error",
            "message": "Unknown role"
        }, dash.no_update

    # =========================================
    # MASTER ADMIN LOGIN FROM NO SOCIETIES PAGE
    # =========================================
    @app.callback(
        Output("session", "data", allow_duplicate=True),
        Output("url", "pathname", allow_duplicate=True),
        Output("toast-store", "data", allow_duplicate=True),
        Output("cookie-store", "data", allow_duplicate=True),
        Input("master-admin-login-btn", "n_clicks"),
        State("master-admin-email", "value"),
        State("master-admin-password", "value"),
        prevent_initial_call=True
    )
    def master_admin_login(n_clicks, email, password):
        if not email or not password:
            return dash.no_update, dash.no_update, {
                "type": "error",
                "message": "Enter the master admin password."
            }, dash.no_update

        user = authenticate_user(email, password)
        if not user or user.get("role") != "admin" or user.get("society_id") is not None:
            return dash.no_update, dash.no_update, {
                "type": "error",
                "message": "Invalid master admin password."
            }, dash.no_update

        user["authenticated"] = True
        return user, "/master", {
            "type": "success",
            "message": "Master admin authenticated. Please add a society."
        }, {}

    # =========================================
    # SOCIETY LOGIN - PIN METHOD
    # =========================================
    @app.callback(
        Output("session", "data", allow_duplicate=True),
        Output("url", "pathname", allow_duplicate=True),
        Output("toast-store", "data", allow_duplicate=True),
        Output("cookie-store", "data", allow_duplicate=True),
        Input("login-pin-btn", "n_clicks"),
        State("login-email-pin", "value"),
        State("login-pin", "value"),
        State("session", "data"),
        State("remember-me-checkbox", "value"),
        prevent_initial_call=True
    )
    def pin_login(n_clicks, email, pin, session_data, remember):
        """Authenticate with email/PIN method."""
        if not email or not pin:
            return dash.no_update, dash.no_update, {
                "type": "error",
                "message": "Enter email and PIN"
            }, dash.no_update

        society_id = session_data.get("society_id") if session_data else None
        user = authenticate_pin(email, pin, society_id)

        if not user:
            return dash.no_update, dash.no_update, {
                "type": "error",
                "message": "Invalid email or PIN"
            }, dash.no_update

        # Successful login - set full session
        user["authenticated"] = True
        
        # Store preferences in local cookie-store
        cookie_data = {"email": email, "society_id": society_id, "method": "pin"} if remember else dash.no_update

        if user.get("role") == "admin" and user.get("society_id") is None:
            return user, "/master", {"type": "success", "message": "Master Admin Login"}, cookie_data

        role = user["role"]
        if role == "admin":
            return user, "/admin", {"type": "success", "message": "Login successful"}, cookie_data
        if role == "apartment":
            return user, "/apartment", {"type": "success", "message": "Login successful"}, cookie_data
        if role == "vendor":
            return user, "/vendor", {"type": "success", "message": "Login successful"}, cookie_data
        if role == "security":
            return user, "/security", {"type": "success", "message": "Login successful"}, cookie_data

        return dash.no_update, dash.no_update, {
            "type": "error",
            "message": "Unknown role"
        }, dash.no_update

    # =========================================
    # SOCIETY LOGIN - PATTERN METHOD
    # =========================================
    @app.callback(
        Output("session", "data", allow_duplicate=True),
        Output("url", "pathname", allow_duplicate=True),
        Output("toast-store", "data", allow_duplicate=True),
        Output("cookie-store", "data", allow_duplicate=True),
        Input("login-pattern-btn", "n_clicks"),
        State("login-email-pattern", "value"),
        State("login-pattern", "value"),
        State("session", "data"),
        State("remember-me-checkbox", "value"),
        prevent_initial_call=True
    )
    def pattern_login(n_clicks, email, pattern, session_data, remember):
        """Authenticate with email/9-dot pattern method."""
        if not email or not pattern:
            return dash.no_update, dash.no_update, {
                "type": "error",
                "message": "Enter email and pattern"
            }, dash.no_update

        society_id = session_data.get("society_id") if session_data else None
        user = authenticate_pattern(email, pattern, society_id)

        if not user:
            return dash.no_update, dash.no_update, {
                "type": "error",
                "message": "Invalid email or pattern"
            }, dash.no_update

        # Successful login - set full session
        user["authenticated"] = True
        
        # Store preferences in local cookie-store
        cookie_data = {"email": email, "society_id": society_id, "method": "pattern"} if remember else dash.no_update

        if user.get("role") == "admin" and user.get("society_id") is None:
            return user, "/master", {"type": "success", "message": "Master Admin Login"}, cookie_data

        role = user["role"]
        if role == "admin":
            return user, "/admin", {"type": "success", "message": "Login successful"}, cookie_data
        if role == "apartment":
            return user, "/apartment", {"type": "success", "message": "Login successful"}, cookie_data
        if role == "vendor":
            return user, "/vendor", {"type": "success", "message": "Login successful"}, cookie_data
        if role == "security":
            return user, "/security", {"type": "success", "message": "Login successful"}, cookie_data

        return dash.no_update, dash.no_update, {
            "type": "error",
            "message": "Unknown role"
        }, dash.no_update

    # =========================================
    # LOGOUT CALLBACK
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
    # ROUTER (MAIN ROUTING LOGIC)
    # =========================================
    @app.callback(
        Output("page-content", "children"),
        Output("navbar", "children"),
        Input("url", "pathname"),
        Input("session", "data"),
        Input("cookie-store", "data"),
        # Input("dummy", "data"), # Ensure dcc.Store(id="dummy") exists in app.layout
        prevent_initial_call=False
    )
    def route(pathname, session_data, cookie_data):

        try:
            print("ROUTER CALLED: pathname =", pathname, "session =", session_data, "cookie =", cookie_data)
        
            # 🔴 NOT LOGGED IN (no role field)
            if not session_data or "role" not in session_data:
                # User has selected a society but not logged in yet
                if session_data and session_data.get("society_id"):
                    society_id = session_data.get("society_id")
                    try:
                        society = get_society_details(society_id)
                        return society_login_layout(
                            society_name=society.get("name", "EstateHub") if society else "EstateHub",
                            society_logo=society.get("logo") if society else None,
                            society_background=society.get("background") if society else None
                        ), ""
                    except Exception as e:
                        print("Error getting society details:", e)
                        # Fallback to society selection
                        try:
                            societies = get_societies()
                            if not societies:
                                return society_select_layout([], error_message="No societies found. Please contact support.", show_master_login=True), ""
                            return society_select_layout(societies), ""
                        except Exception as err:
                            print("Society load exception:", err)
                            return html.Div([
                                html.H2("Error Loading Societies"),
                                html.P(f"Database Error: {str(err)}"),
                                html.P("Please refresh the page or contact support.")
                            ], style={"padding": "20px"}), ""
                
                # Check if we have cookie data with saved email and society
                elif cookie_data and cookie_data.get("email") and cookie_data.get("society_id"):
                    # Second login - user has saved society, go directly to society login
                    society_id = cookie_data.get("society_id")
                    try:
                        society = get_society_details(society_id)
                        return society_login_layout(
                            society_name=society.get("name", "EstateHub") if society else "EstateHub",
                            society_logo=society.get("logo") if society else None,
                            society_background=society.get("background") if society else None
                        ), ""
                    except Exception as err:
                        # Fallback to society selection
                        try:
                            societies = get_societies()
                            if not societies:
                                return society_select_layout([], error_message="No societies found. Please contact support.", show_master_login=True), ""
                            return society_select_layout(societies), ""
                        except Exception as err:
                            print("Society load exception:", err)
                            return html.Div([
                                html.H2("Error Loading Societies"),
                                html.P(f"Database Error: {str(err)}"),
                                html.P("Please refresh the page or contact support.")
                            ], style={"padding": "20px"}), ""
                
                else:
                    # First login - show society selection
                    try:
                        societies = get_societies()
                        if not societies:
                            return society_select_layout([], error_message="No societies found. Please contact support.", show_master_login=True), ""
                        return society_select_layout(societies), ""
                    except Exception as err:
                        print("Society load exception:", err)
                        return html.Div([
                            html.H2("Error Loading Societies"),
                            html.P(f"Database Error: {str(err)}"),
                            html.P("Please refresh the page or contact support.")
                        ], style={"padding": "20px"}), ""

            # 🟢 LOGGED IN - Show navbar
            from ui.components.navbar import get_navbar
            navbar = get_navbar(session_data)

            role = session_data.get("role")
            user_id = session_data.get("user_id")
            society_id = session_data.get("society_id")

            # 🟢 MASTER ADMIN
            if pathname == "/master":
                if role == "admin" and society_id is None:
                    return master_layout(), navbar
                return "❌ Unauthorized", navbar

            # 🟢 SOCIETY ADMIN
            if pathname == "/admin":
                if role == "admin" and society_id is not None:
                    try:
                        data = get_dashboard_metrics(society_id)
                        return admin_layout_dynamic(data), navbar
                    except Exception as e:
                        return html.Div(f"Dashboard Error: {str(e)}"), navbar
                return "❌ Unauthorized", navbar

            # 🟢 OTHER ROLES
            if pathname == "/apartment":
                return (apartment_layout() if role == "apartment" else "❌ Unauthorized"), navbar

            if pathname == "/vendor":
                return (vendor_layout() if role == "vendor" else "❌ Unauthorized"), navbar

            if pathname == "/security":
                return (security_layout() if role == "security" else "❌ Unauthorized"), navbar

            # 🔁 DEFAULT - Redirect to appropriate dashboard
            if role == "admin" and society_id is None:
                return master_layout(), navbar
            elif role == "admin":
                try:
                    data = get_dashboard_metrics(society_id)
                    return admin_layout_dynamic(data), navbar
                except Exception as e:
                    print(f"Admin Dashboard Load Error: {e}")
                    return html.Div([
                        html.H3("Error loading dashboard"),
                        html.P("Please check your database connection.")
                    ], style={"color": "white", "padding": "20px"}), navbar
            
            # Fallback if no specific route matched
            return login_layout(), navbar
            
        except Exception as e:
            print(f"CRITICAL ROUTER ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            return html.Div([
                html.H2("Critical Error"),
                html.P(f"An unexpected error occurred: {str(e)}"),
                html.P("Please contact support.")
            ], style={"padding": "20px"}), ""