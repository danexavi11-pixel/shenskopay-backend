import os
import requests
from requests.auth import HTTPBasicAuth

# Live Pesapal API URL
PESAPAL_API_URL = "https://www.pesapal.com/API/Payments/SubmitPayment"

# Your keys from Render environment variables
CONSUMER_KEY = os.environ.get("PESAPAL_CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("PESAPAL_CONSUMER_SECRET")

def create_payment(amount, description, reference, phone):
    """
    Create a real Pesapal payment request.
    """
    payload = {
        "amount": amount,
        "description": description,
        "type": "MERCHANT",
        "reference": reference,
        "email": f"{phone}@example.com"  # Pesapal requires an email
    }

    response = requests.post(PESAPAL_API_URL,
                             auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET),
                             json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}
