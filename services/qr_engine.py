def generate_qr_string(role, entity_id):
    return f"{role}:{entity_id}"

def parse_qr(code):
    role, entity_id = code.split(":")
    return role, int(entity_id)