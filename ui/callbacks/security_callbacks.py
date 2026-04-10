from dash.dependencies import Input, Output, State
from services.qr_engine import parse_qr
from services.gate_access_service import handle_scan

def register_security_callbacks(app):

    @app.callback(
        Output("scan-result", "children"),
        Input("scan-btn", "n_clicks"),
        State("qr-input", "value")
    )
    def scan(n, qr):

        if not qr:
            return ""

        role, entity_id = parse_qr(qr)

        result = handle_scan(1, role, entity_id)

        if result == "PASS":
            return "✅ PASS"
        elif result == "FAIL":
            return "❌ FAIL"
        else:
            return result