from dash import Input, Output, html

def register_ui_callbacks(app):

    @app.callback(
        Output("toast-container", "children"),
        Input("toast-store", "data")
    )
    def show_toast(data):
        if not data:
            return ""

        color = "#28a745" if data["type"] == "success" else "#dc3545"

        return html.Div(
            data["message"],
            style={
                "backgroundColor": color,
                "color": "white",
                "padding": "12px 20px",
                "borderRadius": "8px",
                "boxShadow": "0 4px 10px rgba(0,0,0,0.2)",
                "marginBottom": "10px",
                "minWidth": "250px"
            }
        )