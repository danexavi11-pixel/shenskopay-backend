from flask import Flask, request, render_template_string
from detector import detect_number

app = Flask(__name__)

FEE_PERCENTAGE = 0.01

BASE_HTML = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ShenskoPay</title>
<style>
body {
    margin: 0;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    background: #f2f4f8;
}
.container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}
.card {
    background: #ffffff;
    width: 100%;
    max-width: 420px;
    padding: 24px;
    border-radius: 14px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}
h1 {
    text-align: center;
    margin-bottom: 20px;
}
label {
    font-weight: 500;
}
input {
    width: 100%;
    padding: 14px;
    margin-top: 6px;
    margin-bottom: 16px;
    font-size: 16px;
    border-radius: 10px;
    border: 1px solid #ccc;
}
button {
    width: 100%;
    padding: 14px;
    background: #0066ff;
    color: white;
    font-size: 16px;
    border: none;
    border-radius: 10px;
}
p {
    font-size: 15px;
}
</style>
</head>
<body>
<div class="container">
<div class="card">
{{ content }}
</div>
</div>
</body>
</html>
"""

HOME = """
<h1>ShenskoPay</h1>
<form method="post" action="/confirm">
<label>Enter number</label>
<input name="number" required>

<label>Amount (Tsh)</label>
<input name="amount" type="number" required>

<button type="submit">Continue</button>
</form>
"""

CONFIRM = """
<h1>Confirm Payment</h1>
<p><strong>Number:</strong> {{ number }}</p>
<p><strong>Name:</strong> {{ name }}</p>
<p><strong>Provider:</strong> {{ provider }}</p>
<p><strong>Amount:</strong> Tsh {{ amount }}</p>
<p><strong>Fee:</strong> Tsh {{ fee }}</p>
<p><strong>Total:</strong> Tsh {{ total }}</p>

<form method="post" action="/complete">
<input type="hidden" name="number" value="{{ number }}">
<input type="hidden" name="amount" value="{{ amount }}">
<input type="hidden" name="fee" value="{{ fee }}">
<button type="submit">Confirm Payment</button>
</form>
"""

SUCCESS = """
<h1>Payment Successful ✅</h1>
<p>Number: {{ number }}</p>
<p>Amount: Tsh {{ amount }}</p>
<p>Fee: Tsh {{ fee }}</p>
<p>Total Deducted: Tsh {{ total }}</p>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(BASE_HTML, content=HOME)

@app.route("/confirm", methods=["POST"])
def confirm():
    number = request.form["number"]
    amount = float(request.form["amount"])

    detected = detect_number(number) or {}
    name = detected.get("name", "Unknown")
    provider = detected.get("provider", "Unknown")

    fee = round(amount * FEE_PERCENTAGE, 2)
    total = amount + fee

    return render_template_string(
        BASE_HTML,
        content=render_template_string(
            CONFIRM,
            number=number,
            name=name,
            provider=provider,
            amount=amount,
            fee=fee,
            total=total
        )
    )

@app.route("/complete", methods=["POST"])
def complete():
    number = request.form["number"]
    amount = float(request.form["amount"])
    fee = float(request.form["fee"])
    total = amount + fee

    return render_template_string(
        BASE_HTML,
        content=render_template_string(
            SUCCESS,
            number=number,
            amount=amount,
            fee=fee,
            total=total
        )
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
