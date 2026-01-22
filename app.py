from flask import Flask, request, render_template_string
import re

app = Flask(__name__)
FEE_PERCENTAGE = 0.01

def detect_number(value: str):
    value = value.strip()
    if re.fullmatch(r"(0|255)[67]\d{8}", value):
        return {"provider": "Mobile Money", "name": "Recipient Verified"}
    return None

STYLE = """
<style>
* { box-sizing: border-box; }

html, body {
    margin: 0;
    height: 100%;
    font-family: 'Segoe UI', Roboto, sans-serif;
    font-size: 18px;
}

/* BACKGROUND */
body {
    display: flex;
    align-items: center;
    justify-content: center;
    background: #0e1a24;
}

/* CARD */
.card {
    width: 94%;
    max-width: 900px;
    background: #ffffff;
    border-radius: 24px;
    padding: 48px;
    box-shadow: 0 30px 70px rgba(0,0,0,0.55);
}

/* BRAND */
.brand {
    text-align: center;
    font-size: 40px;
    font-weight: 900;
    color: #ff6f00;
    margin-bottom: 8px;
}

.tagline {
    text-align: center;
    font-size: 18px;
    color: #555;
    margin-bottom: 40px;
}

/* FORM */
label {
    font-weight: 700;
    font-size: 18px;
    color: #222;
    display: block;
    margin-bottom: 8px;
}

input {
    width: 100%;
    padding: 20px;
    margin-bottom: 28px;
    border-radius: 16px;
    border: 1.5px solid #ccc;
    font-size: 20px;
}

input:focus {
    outline: none;
    border-color: #ff6f00;
}

/* BUTTON */
button {
    width: 100%;
    padding: 20px;
    border-radius: 18px;
    border: none;
    background: linear-gradient(135deg, #ff6f00, #ffb300);
    color: #fff;
    font-size: 22px;
    font-weight: 900;
    cursor: pointer;
}

button:hover { opacity: 0.96; }

/* INFO */
.info {
    font-size: 20px;
    margin: 14px 0;
}

.total {
    margin-top: 18px;
    font-size: 26px;
    font-weight: 900;
}

/* SUCCESS */
.success {
    text-align: center;
    font-size: 32px;
    font-weight: 900;
    color: #2e7d32;
}

/* MOBILE */
@media (max-width: 600px) {
    .card {
        padding: 32px;
    }
    .brand {
        font-size: 32px;
    }
}
</style>
"""

HOME = """
<!doctype html>
<html>
<head><title>ShenskoPay</title>""" + STYLE + """</head>
<body>
<div class="card">
    <div class="brand">ShenskoPay</div>
    <div class="tagline">Fast • Secure • Trusted Payments</div>

    <form action="/confirm" method="post">
        <label>Recipient Number</label>
        <input name="number" placeholder="07XXXXXXXX" required>

        <label>Amount (TZS)</label>
        <input type="number" name="amount" placeholder="Enter amount" required>

        <button type="submit">Continue</button>
    </form>
</div>
</body>
</html>
"""

CONFIRM = """
<!doctype html>
<html>
<head><title>Confirm</title>""" + STYLE + """</head>
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

SUCCESS = """
<!doctype html>
<html>
<head><title>Success</title>""" + STYLE + """</head>
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
    return render_template_string(HOME)

@app.route("/confirm", methods=["POST"])
def confirm():
    number = request.form["number"]
    amount = float(request.form["amount"])
    detected = detect_number(number)
    fee = round(amount * FEE_PERCENTAGE, 2)
    total = amount + fee
    return render_template_string(
        CONFIRM,
        number=number,
        name=detected["name"] if detected else "Unknown",
        amount=amount,
        fee=fee,
        total=total
    )

@app.route("/complete", methods=["POST"])
def complete():
    number = request.form["number"]
    amount = float(request.form["amount"])
    fee = float(request.form["fee"])
    return render_template_string(
        SUCCESS,
        number=number,
        amount=amount,
        fee=fee,
        total=amount + fee
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
