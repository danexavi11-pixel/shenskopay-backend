from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "service": "ShenskoPay Backend",
        "status": "LIVE",
        "step": "ENTER_NUMBER"
    })

@app.route("/detect", methods=["POST"])
def detect():
    data = request.get_json()

    phone = data.get("phone") if data else None

    if not phone:
        return jsonify({
            "error": "Phone number required"
        }), 400

    return jsonify({
        "phone": phone,
        "network": "DETECTED",
        "next_step": "PAYMENT"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
