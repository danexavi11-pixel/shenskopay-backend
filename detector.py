import re

def detect_number(value: str):
    value = value.strip()

    # Vodacom TZ
    if re.fullmatch(r"(0|255)7[0-9]{8}", value):
        return {"provider": "Vodacom", "name": "James Mwita"}

    # Tigo TZ
    if re.fullmatch(r"(0|255)6[0-9]{8}", value):
        return {"provider": "Tigo", "name": "Asha Juma"}

    # Airtel TZ
    if re.fullmatch(r"(0|255)7[89][0-9]{7}", value):
        return {"provider": "Airtel", "name": "John Peter"}

    # Halotel TZ
    if re.fullmatch(r"(0|255)5[0-9]{8}", value):
        return {"provider": "Halotel", "name": "Fatma Ali"}

    # TTCL TZ
    if re.fullmatch(r"(0|255)2[0-9]{8}", value):
        return {"provider": "TTCL", "name": "Daniel Kim"}

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
