import re

def detect_number(value: str):
    value = value.strip()

    # --- TZ mobile numbers (all major providers) ---
    if re.fullmatch(r"(0|255)[67]\d{8}", value):
        return {"provider": "Vodacom/Tigo/Airtel/Halotel/Mantel/TTCL", "name": "James Mwita"}

    # --- Control numbers (Government / bills) ---
    if re.fullmatch(r"\d{10,15}", value):
        return {"provider": "Government", "name": "TRA Payment"}

    # --- Merchant / Lipa Namba ---
    if re.fullmatch(r"\d{5,7}", value):
        return {"provider": "Merchant", "name": "ABC Store"}

    # --- Bank accounts ---
    if re.fullmatch(r"\d{8,16}", value):
        return {"provider": "Bank", "name": "CRDB Account"}

    # --- Default ---
    return None
