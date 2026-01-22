import base64
import json
import requests
from datetime import datetime, timezone

PESAPAL_BASE_URL = "https://pay.pesapal.com/v3"  # LIVE
# For sandbox later we will switch URL

class PesapalClient:
    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.token = None

    def get_access_token(self):
        url = f"{PESAPAL_BASE_URL}/api/Auth/RequestToken"
        credentials = f"{self.consumer_key}:{self.consumer_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers)
        data = response.json()

        self.token = data.get("token")
        return self.token

    def submit_order(self, amount, phone, description="ShenskoPay Payment"):
        if not self.token:
            self.get_access_token()

        url = f"{PESAPAL_BASE_URL}/api/Transactions/SubmitOrderRequest"

        payload = {
            "id": f"SHENSKO-{int(datetime.now(tz=timezone.utc).timestamp())}",
            "currency": "TZS",
            "amount": amount,
            "description": description,
            "callback_url": "https://shenskopay-backend.onrender.com/complete",
            "notification_id": "",
            "billing_address": {
                "phone_number": phone,
                "country_code": "TZ"
            }
        }

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=payload)
        return response.json()
