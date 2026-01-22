import hashlib, hmac, base64, time, requests
from urllib.parse import urlencode

# Pesapal credentials from environment variables
import os
PESAPAL_CONSUMER_KEY = os.getenv("PESAPAL_KEY")
PESAPAL_CONSUMER_SECRET = os.getenv("PESAPAL_SECRET")
PESAPAL_BASE_URL = "https://demo.pesapal.com/api/v1/"

def generate_signature(params: dict):
    """Generate OAuth-like signature for Pesapal"""
    sorted_items = sorted(params.items())
    encoded = urlencode(sorted_items)
    hashed = hmac.new(PESAPAL_CONSUMER_SECRET.encode(), encoded.encode(), hashlib.sha1)
    return base64.b64encode(hashed.digest()).decode()

def create_payment(reference:str, amount:float, description:str, callback_url:str):
    """Send payment request to Pesapal"""
    params = {
        "reference": reference,
        "amount": amount,
        "description": description,
        "callback_url": callback_url,
        "timestamp": int(time.time())
    }
    signature = generate_signature(params)
    headers = {"Authorization": f"Pesapal {PESAPAL_CONSUMER_KEY}:{signature}"}
    resp = requests.post(f"{PESAPAL_BASE_URL}SendMoney", json=params, headers=headers)
    if resp.status_code==200:
        return resp.json()  # contains payment URL / status
    else:
        raise Exception(f"Pesapal Error: {resp.status_code} {resp.text}")
