from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

FEE_PERCENTAGE = 0.01  # 1% per transaction

# Templates
home_template = """
<!doctype html>
<title>ShenskoPay</title>
<h2 style="font-family:sans-serif;">ShenskoPay</h2>
<form action="/confirm" method="post">
    <label>Enter number:</label><br>
    <input type="text" name="number" required><br><br>
    <label>Enter amount (Tsh):</label><br>
    <input type="number" name="amount" required><br><br>
    <button type="submit">Continue</button>
</form>
"""

confirm_template = """
<!doctype html>
<title>ShenskoPay - Confirm</title>
<h2 style="font-family:sans-serif;">ShenskoPay</h2>
<p>Number detected: {{ number }}</p>
<p>Name: {{ name }}</p>
<p>Provider: {{ provider }}</p>
<p>Amount: Tsh {{ amount }}</p>
<p>Transaction fee: Tsh {{ fee }}</p>
<p>Total to send: Tsh {{ total }}</p>
<form action="/complete" method="post">
    <input type="hidden" name="number" value="{{ number }}">
    <input type="hidden" name="amount" value="{{ amount }}">
    <input type="hidden" name="fee" value="{{ fee }}">
    <button type="submit">Confirm Payment</button>
</form>
"""

success_template = """
<!doctype html>
<title>ShenskoPay - Success</title>
<h2 style="font-family:sans-serif;">Payment Successful ✅</h2>
<p>Number: {{ number }}</p>
<p>Amount Sent: Tsh {{ amount }}</p>
<p>Transaction Fee Collected: Tsh {{ fee }}</p>
<p>Total Deducted: Tsh {{ total }}</p>
"""

# Number detector
def detect_number(value: str):
    value = value.strip()
    # TZ mobile numbers
    if re.fullmatch(r"(0|255)[67]\d{8}", value):
        return {"provider": "Vodacom/Tigo/Airtel/Halotel/Mantel/TTCL", "name": "James Mwita"}
    # Government / Control numbers
    if re.fullmatch(r"\d{10,15}", value):
        return {"provider": "Government", "name": "TRA Payment"}
    # Merchant / Lipa Namba
    if re.fullmatch(r"\d{5,7}", value):
        return {"provider": "Merchant", "name": "ABC Store"}
    # Bank account
    if re.fullmatch(r"\d{8,16}", value):
        return {"provider": "Bank", "name": "CRDB Account"}
    return None

@app.route("/", methods=["GET"])
def home():
    return render_template_string(home_template)

@app.route("/confirm", methods=["POST"])
def confirm():
    number = request.form.get("number")
    amount = float(request.form.get("amount"))
    detected = detect_number(number)
    if detected:
        name = detected["name"]
        provider = detected["provider"]
    else:
        name = "Unknown"
        provider = "Unknown"
    fee = round(amount * FEE_PERCENTAGE, 2)
    total = amount + fee
    return render_template_string(confirm_template,
                                  number=number,
                                  name=name,
                                  provider=provider,
                                  amount=amount,
                                  fee=fee,
                                  total=total)

@app.route("/complete", methods=["POST"])
def complete():
    number = request.form.get("number")
    amount = float(request.form.get("amount"))
    fee = float(request.form.get("fee"))
    total = amount + fee
    # Future: integrate real payment gateway here
    return render_template_string(success_template,
                                  number=number,
                                  amount=amount,
                                  fee=fee,
                                  total=total)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
