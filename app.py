from flask import Flask, request, jsonify
from detector import detect_number

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "brand": "ShenskoPay",
        "message": "Enter a number to pay",
        "step": "INPUT_NUMBER"
    })

@app.route("/detect", methods=["POST"])
def detect():
    data = request.get_json(force=True)
    number = data.get("number", "")

    result = detect_number(number)

    return jsonify({
        "input": number,
        "name": result["name"] if result else "Unknown",
        "provider": result["provider"] if result else "Unknown",
        "next_step": "CONFIRM_AND_PAY" if result else "RETRY"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
