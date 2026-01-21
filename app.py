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
    font-family: system-ui, sans-serif;
    background: #f2f4f8;
}
.container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}
.card {
    background: white;
    width: 100%;
    max-width: 420px;
    padding: 24px;
    border-radius: 14px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}
h1 {
    text-align: center;
}
input, button {
    width: 100%;
    padding: 14px;
    font-size: 16px;
    margin-top: 10px;
}
button {
    background: #0066ff;
    color: white;
    border: none;
    border-radius: 10px;
}
</style>
</head>
<body>
<div class="container">
<div class="card">
{{ content | safe }}
</div>
</div>
</body>
</html>
"""

HOME = """
<h1>ShenskoPay</h1>
<form method="post" action="/confirm">
<input name="number" placeholder="Enter number" required>
<input name="amount" type="number" placeholder="Amount (Tsh)" required>
<button type="submit">Continue</button>
</form>
"""

CONFIRM = """
<h1>Confirm Payment</h1>
<p><b>Number:</b> {{ number }}</p>
<p><b>Name:</b> {{ name }}</p>
<p><b>Provider:</b> {{ provider }}</p>
<p><b>Amount:</b> Tsh {{ amount }}</p>
<p><b>Fee:</b> Tsh {{ fee }}</p>
<p><b>Total:</b> Tsh {{ total }}</p>
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
<p>Total Deducted: Tsh {{ total }}</p>
"""

@app.route("/")
def home():
    return render_template_string(BASE_HTML, content=HOME)

@app.route("/confirm", methods=["POST"])
def confirm():
    number = request.form["number"]
    amount = float(request.form["amount"])
    detected = detect_number(number) or {}
    fee = round(amount * FEE_PERCENTAGE, 2)
    total = amount + fee

    return render_template_string(
        BASE_HTML,
        content=render_template_string(
            CONFIRM,
            number=number,
            name=detected.get("name", "Unknown"),
            provider=detected.get("provider", "Unknown"),
            amount=amount,
            fee=fee,
            total=total
        )
    )

@app.route("/complete", methods=["POST"])
def complete():
    amount = float(request.form["amount"])
    fee = float(request.form["fee"])
    total = amount + fee
    return render_template_string(
        BASE_HTML,
        content=render_template_string(SUCCESS, number=request.form["number"], total=total)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
