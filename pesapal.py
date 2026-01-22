import os
import requests
import base64
import uuid

PESAPAL_BASE_URL = "https://pay.pesapal.com/v3"

CONSUMER_KEY = os.getenv("PESAPAL_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("PESAPAL_CONSUMER_SECRET")

def get_access_token():
    auth = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
    encoded = base64.b64encode(auth.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded}",
        "Accept": "application/json"
    }

    res = requests.post(
        f"{PESAPAL_BASE_URL}/api/Auth/RequestToken",
        headers=headers
    )

    res.raise_for_status()
    return res.json()["token"]

def create_payment(amount, description, callback_url):
    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "id": str(uuid.uuid4()),
        "currency": "TZS",
        "amount": amount,
        "description": description,
        "callback_url": callback_url,
        "notification_id": None
    }

    res = requests.post(
        f"{PESAPAL_BASE_URL}/api/Transactions/SubmitOrderRequest",
        json=payload,
        headers=headers
    )

    res.raise_for_status()
    return res.json()
