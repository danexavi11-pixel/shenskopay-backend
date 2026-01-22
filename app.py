from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

FEE_PERCENTAGE = 0.01  # 1%

def detect_number(value: str):
    value = value.strip()
    if re.fullmatch(r"(0|255)[67]\d{8}", value):
        return {"provider": "Mobile Money", "name": "Recipient Name"}
    return None

BASE_STYLE = """
<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    min-height: 100vh;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background:
        linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)),
        url('https://images.unsplash.com/photo-1605902711622-cfb43c4437d1');
    background-size: cover;
    background-position: center;
    display: flex;
    align-items: center;
    justify-content: center;
}

.card {
    width: 100%;
    max-width: 420px;
    background: #ffffff;
    border-radius: 18px;
    padding: 28px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.35);
}

.brand {
    text-align: center;
    font-size: 28px;
    font-weight: 800;
    color: #ff6f00;
    margin-bottom: 8px;
}

.subtitle {
    text-align: center;
    font-size: 14px;
    color: #666;
    margin-bottom: 24px;
}

label {
    font-size: 14px;
    color: #333;
    font-weight: 600;
}

input {
    width: 100%;
    padding: 14px;
    margin-top: 6px;
    margin-bottom: 18px;
    border-radius: 12px;
    border: 1px solid #ddd;
    font-size: 16px;
}

button {
    width: 100%;
    padding: 15px;
    background: linear-gradient(135deg, #ff6f00, #ff9800);
    border: none;
    border-radius: 14px;
    color: white;
    font-size: 18px;
    font-weight: 700;
    cursor: pointer;
}

button:hover {
    opacity: 0.9;
}

.info {
    font-size: 15px;
    margin: 10px 0;
    color: #333;
}

.total {
    font-weight: 800;
    font-size: 18px;
    margin-top: 12px;
}

.success {
    color: #2e7d32;
    font-weight: 800;
    font-size: 22px;
    text-align: center;
    margin-bottom: 12px;
}

@media (max-width: 360px) {
    .card { padding: 22px; }
    .brand { font-size: 24px; }
}
</style>
"""

HOME_HTML = """
<!doctype html>
<html>
<head>
<title>ShenskoPay</title>
""" + BASE_STYLE + """
</head>
<body>
<div class="card">
    <div class="brand">ShenskoPay</div>
    <div class="subtitle">Fast • Secure • Simple Payments</div>

    <form action="/confirm" method="post">
        <label>Recipient Number</label>
        <input name="number" placeholder="07XXXXXXXX" required>

        <label>Amount (TZS)</label>
        <input type="number" name="amount" placeholder="e.g. 2000" required>

        <button type="submit">Continue</button>
    </form>
</div>
</body>
</html>
"""

CONFIRM_HTML = """
<!doctype html>
<html>
<head>
<title>Confirm Payment</title>
""" + BASE_STYLE + """
</head>
<body>
<div class="card">
    <div class="brand">Confirm Payment</div>

    <div class="info">To: <b>{{ name }}</b></div>
    <div class="info">Number: {{ number }}</div>
    <div class="info">Amount: Tsh {{ amount }}</div>
    <div class="info">Fee: Tsh {{ fee }}</div>
    <div class="total">Total: Tsh {{ total }}</div>

    <form action="/complete" method="post">
        <input type="hidden" name="number" value="{{ number }}">
        <input type="hidden" name="amount" value="{{ amount }}">
        <input type="hidden" name="fee" value="{{ fee }}">
        <button type="submit">Confirm & Pay</button>
    </form>
</div>
</body>
</html>
"""

SUCCESS_HTML = """
<!doctype html>
<html>
<head>
<title>Success</title>
""" + BASE_STYLE + """
</head>
<body>
<div class="card">
    <div class="success">Payment Successful</div>
    <div class="info">Sent to {{ number }}</div>
    <div class="info">Amount: Tsh {{ amount }}</div>
    <div class="info">Fee: Tsh {{ fee }}</div>
    <div class="total">Total: Tsh {{ total }}</div>
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HOME_HTML)

@app.route("/confirm", methods=["POST"])
def confirm():
    number = request.form["number"]
    amount = float(request.form["amount"])
    detected = detect_number(number)
    name = detected["name"] if detected else "Unknown"
    fee = round(amount * FEE_PERCENTAGE, 2)
    total = amount + fee
    return render_template_string(CONFIRM_HTML,
        number=number, name=name, amount=amount, fee=fee, total=total)

@app.route("/complete", methods=["POST"])
def complete():
    number = request.form["number"]
    amount = float(request.form["amount"])
    fee = float(request.form["fee"])
    total = amount + fee
    return render_template_string(SUCCESS_HTML,
        number=number, amount=amount, fee=fee, total=total)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
