"""
JWT-based authentication callbacks for Dash.
Integrates with Flask backend JWT endpoints.
"""

from dash import Input, Output, State
import dash
import requests
from services.auth_service import authenticate_user


def register_jwt_callbacks(app):
    """Register JWT authentication callbacks."""
    
    @app.callback(
        Output("session", "data", allow_duplicate=True),
        Output("url", "pathname", allow_duplicate=True),
        Output("toast-store", "data", allow_duplicate=True),
        Input("jwt-login-btn", "n_clicks"),
        State("jwt-email", "value"),
        State("jwt-password", "value"),
        prevent_initial_call=True
    )
    def jwt_login(n_clicks, email, password):
        """
        Authenticate user via JWT and store token.
        
        Flow:
        1. Send credentials to /auth/start-auth
        2. Receive access_token and refresh_token
        3. Store in localStorage via JavaScript
        4. Update Dash session with user info
        """
        if not email or not password:
            return dash.no_update, dash.no_update, {
                "type": "error",
                "message": "Enter email and password"
            }
        
        try:
            # Call Flask auth endpoint
            response = requests.post(
                "http://localhost:8050/auth/start-auth",
                json={"email": email, "password": password},
                timeout=5
            )
            
            if response.status_code != 200:
                return dash.no_update, dash.no_update, {
                    "type": "error",
                    "message": "Authentication failed"
                }
            
            data = response.json()
            access_token = data.get("access_token")
            user = data.get("user")
            
            # Update session with user info
            user["authenticated"] = True
            user["access_token"] = access_token
            user["refresh_token"] = data.get("refresh_token")
            
            # Return updated session and redirect
            role = user.get("role")
            if role == "admin" and user.get("society_id") is None:
                return user, "/master", {"type": "success", "message": "Master Admin logged in"}
            elif role == "admin":
                return user, "/admin", {"type": "success", "message": "Login successful"}
            elif role == "apartment":
                return user, "/apartment", {"type": "success", "message": "Login successful"}
            else:
                return user, "/", {"type": "success", "message": "Login successful"}
        
        except Exception as e:
            print(f"JWT login error: {e}")
            return dash.no_update, dash.no_update, {
                "type": "error",
                "message": f"Login error: {str(e)}"
            }
    
    @app.callback(
        Output("session", "data", allow_duplicate=True),
        Input("jwt-refresh-token", "n_intervals"),
        State("session", "data"),
        prevent_initial_call=True
    )
    def refresh_token(n_intervals, session_data):
        """
        Refresh access token when it's about to expire.
        This runs every 25 minutes (before 30-minute expiry).
        """
        if not session_data or not session_data.get("refresh_token"):
            return dash.no_update
        
        try:
            response = requests.post(
                "http://localhost:8050/auth/refresh",
                json={"refresh_token": session_data.get("refresh_token")},
                timeout=5
            )
            
            if response.status_code != 200:
                # Token refresh failed, user needs to re-login
                return None
            
            data = response.json()
            new_access_token = data.get("access_token")
            
            # Update session with new token
            session_data["access_token"] = new_access_token
            return session_data
        
        except Exception as e:
            print(f"Token refresh error: {e}")
            return dash.no_update
