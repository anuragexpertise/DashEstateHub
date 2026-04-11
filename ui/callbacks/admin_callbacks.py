from dash import Input, Output, State, html
from services.accounts_service import process_accounts_upload
from services.dashboard_service import get_dashboard_metrics
from services.society_service import create_society_full, get_societies
def register_admin_callbacks(app):

    @app.callback(
        Output("society-output", "children"),
        Input("create-society-btn", "n_clicks"),
        State("soc-name", "value"),
        State("soc-email", "value"),
        State("soc-phone", "value"),
        State("soc-address", "value"),
        State("soc-sec-name", "value"),
        State("soc-sec-phone", "value"),
        State("soc-plan-validity", "date"),
        State("soc-arrear-date", "date")
    )
    def create_soc(n, name, email, phone, address, sec_name, sec_phone, validity, arrear):
        if not n:
            return ""

        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "secretary_name": sec_name,
            "secretary_phone": sec_phone,
            "plan": "Free",
            "plan_validity": validity,
            "arrear_start_date": arrear
        }

        sid = create_society_full(data)

        return f"Society Created with ID: {sid}"
    
    @app.callback(
        Output("upload-status", "children"),
        Input("upload-accounts", "contents"),
        State("session", "data")
    )
    def upload_accounts(contents, session):
        if not contents:
            return ""

        society_id = session.get("society_id")

        return process_accounts_upload(contents, society_id)
    
    @app.callback(
        Output("society-list", "children"),
        Input("create-soc-btn", "n_clicks"),
        State("soc-name", "value"),
        State("soc-email", "value"),
        State("soc-phone", "value"),
        State("admin-email", "value"),
        State("admin-password", "value"),
        prevent_initial_call=True
    )
    def handle_create(n, name, email, phone, admin_email, admin_password):

        if not name or not admin_email or not admin_password:
            return "❌ Missing required fields"

        result = create_society_full({
            "name": name,
            "email": email,
            "phone": phone,
            "admin_email": admin_email,
            "admin_password": admin_password,
            "validity": "2026-12-31"
        })

        if result["status"] == "error":
            return f"❌ {result['message']}"

        societies = get_societies()

        return html.Div([
            html.Div(f"{s[0]} | {s[1]}") for s in societies
        ])