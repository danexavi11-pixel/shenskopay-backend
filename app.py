from flask import Flask, request, jsonify
from detector import detect_number
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "brand": "ShenskoPay",
        "step": "ENTER_NUMBER"
    })

@app.route("/confirm", methods=["POST"])
def confirm():
    data = request.get_json(force=True)
    number = data.get("number", "")

    result = detect_number(number)
    if not result:
        return jsonify({"error": "Invalid number"}), 400

    return jsonify({
        "name": result["name"],
        "provider": result["provider"],
        "step": "ENTER_AMOUNT"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
