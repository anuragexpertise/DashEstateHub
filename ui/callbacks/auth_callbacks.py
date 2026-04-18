from dash import Input, Output, State, html, dcc, no_update
import dash
from services.auth_service import (
    authenticate_user,
    authenticate_pin, 
    authenticate_pattern
)
from services.society_service import get_societies, get_society_details
from services.dashboard_service import get_dashboard_metrics

from ui.pages.login import society_login_layout
from ui.pages.society_select import society_select_layout
from ui.pages.admin import admin_layout_dynamic
from ui.pages.master_admin import layout as master_layout
from ui.pages.apartment import apartment_layout
from ui.pages.vendor import vendor_layout
from ui.pages.security import security_layout


def register_auth_callbacks(app):
    
    # =========================================
    # PRIMARY LOGIN - SOCIETY SELECTION
    # =========================================
    @app.callback(
        Output("auth-store", "data", allow_duplicate=True),
        Output("url", "pathname", allow_duplicate=True),
        Output("toast-store", "data", allow_duplicate=True),
        Output("cookie-store", "data", allow_duplicate=True),
        Input("society-select-btn", "n_clicks"),
        State("society-dropdown", "value"),
        State("remember-society-checkbox", "value"),
        prevent_initial_call=True
    )
    def select_society(n_clicks, society_id, remember_society):
        """Handle society selection from first login page."""
        if not n_clicks or not society_id:
            return no_update, no_update, {
                "type": "error",
                "message": "Please select a society"
            }, no_update

        # Store society selection in auth store
        session_data = {
            "society_id": society_id,
            "authenticated": False,
            "stage": "society_selected"
        }

        # Store in cookie if remember checked
        cookie_update = no_update
        if remember_society and len(remember_society) > 0:
            cookie_update = {"society_id": society_id}

        return session_data, "/society-login", {
            "type": "success",
            "message": "Society selected. Please log in."
        }, cookie_update

    # =========================================
    # LOAD SOCIETY LOGIN PAGE
    # =========================================
    @app.callback(
        Output("society-login-container", "children"),
        Input("url", "pathname"),
        State("auth-store", "data"),
        State("cookie-store", "data"),
        prevent_initial_call=False
    )
    def load_society_login_page(pathname, auth_data, cookie_data):
        """Load the society login page with pre-filled data."""
        
        if pathname != "/society-login":
            return ""
        
        print(f"Loading society login - auth: {auth_data}, cookie: {cookie_data}")
        
        # Get society_id from auth store or cookie
        society_id = None
        prefill_email = None
        prefill_method = "password"
        
        if auth_data and auth_data.get("society_id"):
            society_id = auth_data.get("society_id")
        elif cookie_data and cookie_data.get("society_id"):
            society_id = cookie_data.get("society_id")
            prefill_email = cookie_data.get("email")
            prefill_method = cookie_data.get("method", "password")
        
        # If no society_id, check if any societies exist
        if not society_id:
            try:
                societies = get_societies()
                if not societies:
                    return html.Div([
                        html.H2("No Societies Found", style={"textAlign": "center"}),
                        html.Div([
                            dcc.Input(id="master-admin-email", type="email", 
                                     value="master@estatehub.com", placeholder="Email",
                                     style={"width": "100%", "padding": "10px", "marginBottom": "10px"}),
                            dcc.Input(id="master-admin-password", type="password", 
                                     placeholder="Password",
                                     style={"width": "100%", "padding": "10px", "marginBottom": "10px"}),
                            html.Button("Login as Master Admin", id="master-admin-login-btn",
                                       style={"width": "100%", "padding": "10px"})
                        ], style={"maxWidth": "400px", "margin": "0 auto"})
                    ], style={"padding": "40px"})
            except Exception as e:
                return html.Div([
                    html.H2("Network Error", style={"color": "red"}),
                    html.Button("Retry Connection", id="retry-connection-btn")
                ], style={"padding": "40px"})
        
        # Get society details
        try:
            society = get_society_details(society_id) if society_id else None
            society_name = society.get("name", "EstateHub") if society else "EstateHub"
        except:
            society_name = "EstateHub"
        
        return society_login_layout(
            society_name=society_name,
            prefill_email=prefill_email,
            default_method=prefill_method
        )

    # =========================================
    # SECONDARY LOGIN - PASSWORD METHOD
    # =========================================
    @app.callback(
        Output("auth-store", "data", allow_duplicate=True),
        Output("url", "pathname", allow_duplicate=True),
        Output("toast-store", "data", allow_duplicate=True),
        Output("cookie-store", "data", allow_duplicate=True),
        Input("login-btn", "n_clicks"),
        State("login-email", "value"),
        State("login-password", "value"),
        State("auth-store", "data"),
        State("remember-me-checkbox", "value"),
        prevent_initial_call=True
    )
    def password_login(n_clicks, email, password, auth_data, remember):
        """Authenticate with email/password method."""
        if not n_clicks:
            return no_update, no_update, no_update, no_update
            
        if not email or not password:
            return no_update, no_update, {
                "type": "error",
                "message": "Enter email and password"
            }, no_update

        # Get society_id from auth store
        society_id = auth_data.get("society_id") if auth_data else None
        
        print(f"\n=== PASSWORD LOGIN ATTEMPT ===")
        print(f"Email: {email}")
        print(f"Society ID: {society_id}")
        
        user = authenticate_user(email, password, society_id)

        if not user:
            print("Authentication FAILED")
            return no_update, no_update, {
                "type": "error",
                "message": "Invalid email or password"
            }, no_update

        print(f"Authentication SUCCESS")
        print(f"User role: {user.get('role')}")
        print(f"User society_id: {user.get('society_id')}")

        # Create complete session data
        complete_session = {
            "user_id": user.get("user_id"),
            "email": user.get("email"),
            "role": user.get("role"),
            "society_id": user.get("society_id") or society_id,
            "authenticated": True,
            "stage": "logged_in"
        }
        
        print(f"Complete session: {complete_session}")
        
        # Store in cookie if remember me
        cookie_data = no_update
        if remember and len(remember) > 0:
            cookie_data = {
                "email": email, 
                "society_id": society_id, 
                "method": "password"
            }

        # Determine redirect path
        role = user.get("role")
        
        if role == "admin" and user.get("society_id") is None:
            redirect_path = "/master"
            message = "Master Admin Login"
        elif role == "admin":
            redirect_path = "/admin"
            message = "Welcome to Admin Dashboard"
        elif role == "apartment":
            redirect_path = "/apartment"
            message = "Welcome to Apartment Dashboard"
        elif role == "vendor":
            redirect_path = "/vendor"
            message = "Welcome to Vendor Dashboard"
        elif role == "security":
            redirect_path = "/security"
            message = "Welcome to Security Dashboard"
        else:
            redirect_path = "/"
            message = "Login successful"

        print(f"Redirecting to: {redirect_path}")
        print(f"=============================\n")
        
        return complete_session, redirect_path, {
            "type": "success",
            "message": message
        }, cookie_data

    # =========================================
    # PIN LOGIN
    # =========================================
    @app.callback(
        Output("auth-store", "data", allow_duplicate=True),
        Output("url", "pathname", allow_duplicate=True),
        Output("toast-store", "data", allow_duplicate=True),
        Output("cookie-store", "data", allow_duplicate=True),
        Input("login-pin-btn", "n_clicks"),
        State("login-email-pin", "value"),
        State("login-pin", "value"),
        State("auth-store", "data"),
        State("remember-me-checkbox", "value"),
        prevent_initial_call=True
    )
    def pin_login(n_clicks, email, pin, auth_data, remember):
        """Authenticate with email/PIN method."""
        if not n_clicks:
            return no_update, no_update, no_update, no_update
            
        if not email or not pin:
            return no_update, no_update, {
                "type": "error",
                "message": "Enter email and PIN"
            }, no_update

        society_id = auth_data.get("society_id") if auth_data else None
        user = authenticate_pin(email, pin, society_id)

        if not user:
            return no_update, no_update, {
                "type": "error",
                "message": "Invalid email or PIN"
            }, no_update

        complete_session = {
            "user_id": user.get("user_id"),
            "email": user.get("email"),
            "role": user.get("role"),
            "society_id": user.get("society_id") or society_id,
            "authenticated": True,
            "stage": "logged_in"
        }

        cookie_data = no_update
        if remember and len(remember) > 0:
            cookie_data = {
                "email": email, 
                "society_id": society_id, 
                "method": "pin"
            }

        role = user.get("role")
        if role == "admin" and user.get("society_id") is None:
            redirect_path = "/master"
        elif role == "admin":
            redirect_path = "/admin"
        elif role == "apartment":
            redirect_path = "/apartment"
        elif role == "vendor":
            redirect_path = "/vendor"
        elif role == "security":
            redirect_path = "/security"
        else:
            redirect_path = "/"

        return complete_session, redirect_path, {
            "type": "success",
            "message": f"Welcome back, {email}"
        }, cookie_data

    # =========================================
    # PATTERN LOGIN
    # =========================================
    @app.callback(
        Output("auth-store", "data", allow_duplicate=True),
        Output("url", "pathname", allow_duplicate=True),
        Output("toast-store", "data", allow_duplicate=True),
        Output("cookie-store", "data", allow_duplicate=True),
        Input("login-pattern-btn", "n_clicks"),
        State("login-email-pattern", "value"),
        State("login-pattern", "value"),
        State("auth-store", "data"),
        State("remember-me-checkbox", "value"),
        prevent_initial_call=True
    )
    def pattern_login(n_clicks, email, pattern, auth_data, remember):
        """Authenticate with pattern method."""
        if not n_clicks:
            return no_update, no_update, no_update, no_update
            
        if not email or not pattern:
            return no_update, no_update, {
                "type": "error",
                "message": "Enter email and pattern"
            }, no_update

        society_id = auth_data.get("society_id") if auth_data else None
        user = authenticate_pattern(email, pattern, society_id)

        if not user:
            return no_update, no_update, {
                "type": "error",
                "message": "Invalid email or pattern"
            }, no_update

        complete_session = {
            "user_id": user.get("user_id"),
            "email": user.get("email"),
            "role": user.get("role"),
            "society_id": user.get("society_id") or society_id,
            "authenticated": True,
            "stage": "logged_in"
        }

        cookie_data = no_update
        if remember and len(remember) > 0:
            cookie_data = {
                "email": email, 
                "society_id": society_id, 
                "method": "pattern"
            }

        role = user.get("role")
        if role == "admin" and user.get("society_id") is None:
            redirect_path = "/master"
        elif role == "admin":
            redirect_path = "/admin"
        elif role == "apartment":
            redirect_path = "/apartment"
        elif role == "vendor":
            redirect_path = "/vendor"
        elif role == "security":
            redirect_path = "/security"
        else:
            redirect_path = "/"

        return complete_session, redirect_path, {
            "type": "success",
            "message": f"Welcome back, {email}"
        }, cookie_data

    # =========================================
    # MASTER ADMIN LOGIN
    # =========================================
    @app.callback(
        Output("auth-store", "data", allow_duplicate=True),
        Output("url", "pathname", allow_duplicate=True),
        Output("toast-store", "data", allow_duplicate=True),
        Input("master-admin-login-btn", "n_clicks"),
        State("master-admin-email", "value"),
        State("master-admin-password", "value"),
        prevent_initial_call=True
    )
    def master_admin_login(n_clicks, email, password):
        if not n_clicks:
            return no_update, no_update, no_update
            
        if not email or not password:
            return no_update, no_update, {
                "type": "error",
                "message": "Enter email and password"
            }

        user = authenticate_user(email, password)
        if not user or user.get("role") != "admin" or user.get("society_id") is not None:
            return no_update, no_update, {
                "type": "error",
                "message": "Invalid master admin credentials"
            }

        complete_session = {
            "user_id": user.get("user_id"),
            "email": user.get("email"),
            "role": "admin",
            "society_id": None,
            "authenticated": True,
            "stage": "logged_in"
        }
        
        return complete_session, "/master", {
            "type": "success",
            "message": "Master admin authenticated"
        }

    # =========================================
    # LOGOUT
    # =========================================
    @app.callback(
        Output("auth-store", "data", allow_duplicate=True),
        Output("url", "pathname", allow_duplicate=True),
        Output("toast-store", "data", allow_duplicate=True),
        Input("logout-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def logout_handler(n_clicks):
        if not n_clicks:
            return no_update, no_update, no_update
        
        return None, "/", {
            "type": "success",
            "message": "Logged out successfully"
        }

    # =========================================
    # MAIN ROUTER - Uses auth-store for persistent session
    # =========================================
    @app.callback(
        Output("page-content", "children"),
        Output("navbar", "children"),
        Input("url", "pathname"),
        State("auth-store", "data"),
        prevent_initial_call=False
    )
    def router(pathname, auth_data):
        """Main routing logic using persistent auth store."""
        
        print(f"\n=== ROUTER ===")
        print(f"Pathname: {pathname}")
        print(f"Auth data: {auth_data}")
        
        from ui.components.navbar import get_navbar
        
        # Not authenticated - show society selection
        if not auth_data or not auth_data.get("authenticated"):
            print("Not authenticated - showing society selection")
            
            # Don't override society-login page
            if pathname == "/society-login":
                return "", ""
            
            try:
                societies = get_societies()
                if not societies:
                    return society_select_layout([], show_master_login=True), ""
                return society_select_layout(societies), ""
            except Exception as err:
                print(f"Error: {err}")
                return html.Div([
                    html.H2("Network Error", style={"color": "red", "textAlign": "center"}),
                    html.P("Unable to connect to the database.", style={"textAlign": "center"}),
                    html.Button("Retry Connection", id="retry-connection-btn",
                               style={"display": "block", "margin": "20px auto", "padding": "10px 20px"})
                ]), ""
        
        # Authenticated - show appropriate dashboard
        print("Authenticated - showing dashboard")
        navbar = get_navbar(auth_data)
        
        role = auth_data.get("role")
        society_id = auth_data.get("society_id")
        
        # Route to appropriate dashboard
        if role == "admin" and society_id is None:
            return master_layout(), navbar
        elif role == "admin":
            try:
                data = get_dashboard_metrics(society_id)
                return admin_layout_dynamic(data), navbar
            except Exception as e:
                return html.Div(f"Dashboard Error: {str(e)}", style={"padding": "20px"}), navbar
        elif role == "apartment":
            return apartment_layout(), navbar
        elif role == "vendor":
            return vendor_layout(), navbar
        elif role == "security":
            return security_layout(), navbar
        
        return html.Div(f"Unknown role: {role}", style={"padding": "20px"}), navbar
    
    # =========================================
    # RETRY CONNECTION
    # =========================================
    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        Output("toast-store", "data", allow_duplicate=True),
        Input("retry-connection-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def retry_connection(n_clicks):
        if not n_clicks:
            return no_update, no_update
        
        try:
            get_societies()
            return "/", {"type": "success", "message": "Connection restored!"}
        except Exception as e:
            return "/", {"type": "error", "message": f"Still unable to connect: {str(e)}"}