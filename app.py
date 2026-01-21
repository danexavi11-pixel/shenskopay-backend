from flask import Flask, request, jsonify
import os
import re

app = Flask(__name__)

def detect_number(value: str):
    value = value.strip()

    if re.fullmatch(r"(0|255)[67]\d{8}", value):
        return {"provider": "Vodacom", "name": "James Mwita"}

    if re.fullmatch(r"\d{10,15}", value):
        return {"provider": "Government", "name": "TRA Payment"}

    if re.fullmatch(r"\d{5,7}", value):
        return {"provider": "Merchant", "name": "ABC Store"}

    if re.fullmatch(r"\d{8,16}", value):
        return {"provider": "Bank", "name": "CRDB Account"}

    return None


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "brand": "ShenskoPay",
        "step": "ENTER_NUMBER"
    })


@app.route("/confirm", methods=["POST"])
def confirm():
    data = request.get_json()
    number = data.get("number", "")

    result = detect_number(number)

    if not result:
        return jsonify({"error": "Invalid number"}), 400

    return jsonify({
        "name": result["name"],
        "provider": result["provider"],
        "next": "ENTER_AMOUNT"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
