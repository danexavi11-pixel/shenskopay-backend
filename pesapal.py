import requests
import base64
import uuid
import json

PESAPAL_CONSUMER_KEY = "PUT_YOUR_KEY_HERE"
PESAPAL_CONSUMER_SECRET = "PUT_YOUR_SECRET_HERE"

PESAPAL_BASE_URL = "https://pay.pesapal.com/v3"

def get_access_token():
    auth_string = f"{PESAPAL_CONSUMER_KEY}:{PESAPAL_CONSUMER_SECRET}"
    encoded = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json"
    }

    res = requests.post(
        f"{PESAPAL_BASE_URL}/api/Auth/RequestToken",
        headers=headers
    )

    return res.json()["token"]


def create_payment(amount, currency, description, callback_url):
    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    order_id = str(uuid.uuid4())

    payload = {
        "id": order_id,
        "currency": currency,
        "amount": amount,
        "description": description,
        "callback_url": callback_url,
        "notification_id": None
    }

    res = requests.post(
        f"{PESAPAL_BASE_URL}/api/Transactions/SubmitOrderRequest",
        headers=headers,
        data=json.dumps(payload)
    )

    return res.json()
