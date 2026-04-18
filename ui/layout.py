from dash import html, dcc

def serve_layout():
    return html.Div([

        dcc.Location(id="url", refresh=False),  # Set refresh=False to prevent page reloads
        
        # Use localStorage for persistent storage across page reloads
        dcc.Store(id="auth-store", storage_type="local"),  # This persists across reloads
        dcc.Store(id="temp-store", storage_type="memory"),  # For temporary data
        dcc.Store(id="toast-store", storage_type="memory"),
        dcc.Store(id="cookie-store", storage_type="local"),

        # Toast container
        html.Div(id="toast-container", style={
            "position": "fixed",
            "top": "20px",
            "right": "20px",
            "zIndex": "9999"
        }),

        # Navbar
        html.Div(id="navbar"),

        # Page content
        html.Div(id="page-content"),
        
        # Container for society login page
        html.Div(id="society-login-container"),
        
        # Hidden div to trigger route changes
        html.Div(id="route-trigger", style={"display": "none"}),
        
        # JavaScript to prevent page reload on navigation
        html.Script("""
            // Intercept link clicks to prevent full page reloads
            document.addEventListener('click', function(e) {
                if (e.target.tagName === 'A' && e.target.getAttribute('href')) {
                    const href = e.target.getAttribute('href');
                    if (href.startsWith('/') && !href.startsWith('//')) {
                        e.preventDefault();
                        // Use Dash's built-in navigation
                        if (window.dash_clientside && window.dash_clientside.clientside) {
                            // This will trigger Dash navigation
                            window.dash_clientside.setProps('url', {pathname: href});
                        }
                    }
                }
            });
        """),
        
        html.Script(src="/assets/push.js")

    ], style={
        "fontFamily": "Segoe UI, sans-serif",
        "minHeight": "100vh"
    })