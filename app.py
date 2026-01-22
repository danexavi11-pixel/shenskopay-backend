from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

FEE_PERCENTAGE = 0.01

def detect_number(value: str):
    value = value.strip()
    if re.fullmatch(r"(0|255)[67]\d{8}", value):
        return {"provider": "Mobile Money", "name": "Recipient Verified"}
    return None

BASE_STYLE = """
<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    min-height: 100vh;
    font-family: 'Segoe UI', Roboto, sans-serif;
    background:
        radial-gradient(circle at top, #ff9800 0%, transparent 60%),
        linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

/* MAIN CARD */
.card {
    width: 100%;
    max-width: 720px;
    background: linear-gradient(
        180deg,
        rgba(255,255,255,0.95),
        rgba(245,245,245,0.92)
    );
    border-radius: 22px;
    padding: 36px;
    box-shadow: 0 30px 60px rgba(0,0,0,0.45);
}

/* BRAND */
.brand {
    text-align: center;
    font-size: 34px;
    font-weight: 900;
    color: #ff6f00;
    letter-spacing: 1px;
}

.tagline {
    text-align: center;
    font-size: 15px;
    color: #555;
    margin-bottom: 30px;
}

/* FORM */
label {
    font-size: 15px;
    font-weight: 700;
    color: #222;
}

input {
    width: 100%;
    padding: 16px;
    margin-top: 8px;
    margin-bottom: 22px;
    border-radius: 14px;
    border: 1px solid #ccc;
    font-size: 17px;
}

button {
    width: 100%;
    padding: 18px;
    border: none;
    border-radius: 16px;
    background: linear-gradient(135deg, #ff6f00, #ffb300);
    color: #fff;
    font-size: 19px;
    font-weight: 800;
    cursor: pointer;
}

button:hover {
    opacity: 0.95;
}

/* INFO */
.info {
    font-size: 17px;
    margin: 10px 0;
    color: #333;
}

.total {
    margin-top: 14px;
    font-size: 20px;
    font-weight: 900;
}

/* SUCCESS */
.success {
    text-align: center;
    font-size: 26px;
    font-weight: 900;
    color: #2e7d32;
    margin-bottom: 16px;
}

/* MOBILE */
@media (max-width: 600px) {
    .card {
        padding: 26px;
        max-width: 100%;
    }
    .brand {
        font-size: 28px;
    }
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
    <div class="tagline">Pay Anyone. Anywhere. Instantly.</div>

    <form action="/confirm" method="post">
        <label>Recipient Number</label>
        <input name="number" placeholder="07XXXXXXXX" required>

        <label>Amount (TZS)</label>
        <input type="number" name="amount" placeholder="e.g. 5000" required>

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

    <div class="info">Recipient: <b>{{ name }}</b></div>
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
    <div class="info">To: {{ number }}</div>
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
    return render_template_string(
        CONFIRM_HTML,
        number=number,
        name=name,
        amount=amount,
        fee=fee,
        total=total
    )

@app.route("/complete", methods=["POST"])
def complete():
    number = request.form["number"]
    amount = float(request.form["amount"])
    fee = float(request.form["fee"])
    total = amount + fee
    return render_template_string(
        SUCCESS_HTML,
        number=number,
        amount=amount,
        fee=fee,
        total=total
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
