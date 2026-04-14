"""
Society Selection Page - First step in two-stage login
User selects their society, email is stored in browser cookie for next visit
"""
from dash import html, dcc


def society_select_layout(societies_list=None):
    """
    Main society selection page shown on first login.
    
    Args:
        societies_list: List of dict with {id, name, logo} for dropdown
    
    Returns:
        Dash layout component
    """
    if not societies_list:
        societies_list = []
    
    options = [{"label": s.get("name", "Unknown"), "value": s.get("id")} for s in societies_list]
    
    return html.Div([
        # Background overlay
        html.Div(style={
            "position": "fixed",
            "top": "0",
            "left": "0",
            "width": "100%",
            "height": "100%",
            "backgroundImage": "url('/assets/estate_management_light.jpg')",
            "backgroundSize": "cover",
            "backgroundPosition": "center",
            "filter": "brightness(0.6)",
            "zIndex": "-1"
        }),

        # Main card
        html.Div([
            html.Div([
                html.H1("Welcome to EstateHub", className="society-select-title"),
                html.P("Select your society to continue", className="society-select-subtitle")
            ], className="society-select-header"),

            html.Div([
                # Dropdown for society selection
                dcc.Dropdown(
                    id="society-dropdown",
                    options=options,
                    placeholder="Choose your society...",
                    clearable=False,
                    className="society-dropdown",
                    style={
                        "marginBottom": "20px"
                    }
                ),

                # Remember checkbox
                html.Div([
                    html.Label([
                        dcc.Checklist(
                            id="remember-society-checkbox",
                            options=[{"label": " Remember this society (not needed every login)", "value": 1}],
                            value=[],
                            style={"display": "inline-block"}
                        )
                    ], style={"color": "rgba(255,255,255,0.8)", "fontSize": "0.95rem"})
                ], style={"marginBottom": "20px"}),

                # Continue button
                html.Button(
                    "Continue to Login",
                    id="society-select-btn",
                    className="btn-glass",
                    style={"width": "100%", "marginBottom": "15px"}
                ),

                # Master Admin Login button
                html.Button(
                    "Master Admin Login",
                    id="master-admin-btn",
                    className="btn-glass-secondary",
                    style={"width": "100%", "marginBottom": "20px"}
                ),

                # Help text
                html.Div([
                    html.P("First time? Contact your society admin for access.", 
                           style={"marginTop": "10px", "color": "rgba(255,255,255,0.6)", "fontSize": "0.9rem"})
                ])
            ], className="society-select-form")
        ], className="society-select-card glass")
    ], className="society-select-page")
