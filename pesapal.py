import requests
import base64
import uuid
import json
import os

PESAPAL_CONSUMER_KEY = os.environ.get("PESAPAL_CONSUMER_KEY")
PESAPAL_CONSUMER_SECRET = os.environ.get("PESAPAL_CONSUMER_SECRET")

PESAPAL_BASE_URL = "https://pay.pesapal.com/v3"

def get_access_token():
    if not PESAPAL_CONSUMER_KEY or not PESAPAL_CONSUMER_SECRET:
        raise Exception("Pesapal keys not set in environment variables")

    auth_string = f"{PESAPAL_CONSUMER_KEY}:{PESAPAL_CONSUMER_SECRET}"
    encoded = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json"
    }

    res = requests.post(
        f"{PESAPAL_BASE_URL}/api/Auth/RequestToken",
        headers=headers,
        timeout=15
    )

    data = res.json()
    if "token" not in data:
        raise Exception(f"Pesapal auth failed: {data}")

    return data["token"]


def create_payment(amount, currency, description, callback_url):
    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "id": str(uuid.uuid4()),
        "currency": currency,
        "amount": amount,
        "description": description,
        "callback_url": callback_url
    }

    res = requests.post(
        f"{PESAPAL_BASE_URL}/api/Transactions/SubmitOrderRequest",
        headers=headers,
        json=payload,
        timeout=15
    )

    data = res.json()
    if "redirect_url" not in data:
        raise Exception(f"Pesapal order failed: {data}")

    return data
