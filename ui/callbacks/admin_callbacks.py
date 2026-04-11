from dash import Input, Output, State
from services.society_service import create_society
from services.accounts_service import process_accounts_upload
from services.dashboard_service import get_dashboard_metrics

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

        sid = create_society(data)

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
    
    