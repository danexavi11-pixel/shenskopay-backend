import re

def detect_number(value: str):
    value = value.strip()

    # TZ mobile numbers (examples)
    if re.fullmatch(r"(0|255)[67]\d{8}", value):
        return {"provider": "Vodacom", "name": "James Mwita"}
    if re.fullmatch(r"(0|255)68\d{8}", value):
        return {"provider": "Airtel", "name": "Airtel User"}
    if re.fullmatch(r"(0|255)65\d{8}", value):
        return {"provider": "Tigo", "name": "Tigo User"}
    if re.fullmatch(r"(0|255)62\d{8}", value):
        return {"provider": "TTCL", "name": "TTCL User"}
    if re.fullmatch(r"(0|255)66\d{8}", value):
        return {"provider": "Halotel", "name": "Halotel User"}

    # Control numbers (gov / bills)
    if re.fullmatch(r"\d{10,15}", value):
        return {"provider": "Government", "name": "TRA Payment"}

    # Merchant / Lipa Namba
    if re.fullmatch(r"\d{5,7}", value):
        return {"provider": "Merchant", "name": "ABC Store"}

    # Bank account
    if re.fullmatch(r"\d{8,16}", value):
        return {"provider": "Bank", "name": "CRDB Account"}

    return None
