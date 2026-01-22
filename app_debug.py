from flask import Flask, request, render_template_string, redirect, url_for
from detector import detect_number
from pesapal import create_payment

app = Flask(__name__)

FEE_PERCENTAGE = 0.01  # 1% fee per transaction

home_template = """..."""   # keep your existing HTML templates
confirm_template = """..."""
success_template = """..."""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(home_template)

@app.route("/confirm", methods=["POST"])
def confirm():
    number = request.form.get("number")
    amount = float(request.form.get("amount"))
    detected = detect_number(number)
    name = detected["name"] if detected else "Unknown"
    provider = detected["provider"] if detected else "Unknown"
    fee = round(amount * FEE_PERCENTAGE, 2)
    total = amount + fee
    return render_template_string(confirm_template, number=number, name=name, provider=provider, amount=amount, fee=fee, total=total)

@app.route("/complete", methods=["POST"])
def complete():
    number = request.form.get("number")
    amount = float(request.form.get("amount"))
    fee = float(request.form.get("fee"))
    total = amount + fee

    try:
        payment = create_payment(amount, "TZS", f"Payment to {number}", "http://localhost:5000/complete")
        return f"Pesapal redirect URL: {payment.get('redirect_url')}"
    except Exception as e:
        return f"ERROR: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
