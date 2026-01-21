from flask import Flask, request, render_template_string
from detector import detect_number

app = Flask(__name__)

FEE_PERCENTAGE = 0.01  # 1% fee

BASE_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<style>
body {
    margin: 0;
    padding: 0;
    background: #f4f6f8;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
    max-width: 380px;
    padding: 24px;
    border-radius: 14px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

h1 {
    text-align: center;
    margin-bottom: 20px;
    font-size: 22px;
}

label {
    font-size: 14px;
    color: #333;
}

input {
    width: 100%;
    padding: 12px;
    margin-top: 6px;
    margin-bottom: 14px;
    font-size: 16px;
    border-radius: 8px;
    border: 1px solid #ccc;
}

button {
    width: 100%;
    padding: 14px;
    background: #0a7cff;
    color: white;
    font-size: 16px;
    border: none;
    border-radius: 10px;
    cursor: pointer;
}

button:hover {
    background: #055fd4;
}

.info {
    font-size: 15px;
    margin-bottom: 8px;
}
.total {
    font-weight: bold;
    margin-top: 10px;
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

HOME_CONTENT = """
<h1>ShenskoPay</h1>
<form method="post" action="/confirm">
<label>Phone / Number</label>
<input type="text" name="number" required>

<label>Amount (TSh)</label>
<input type="number" name="amount" required>

<button type="submit">Continue</button>
</form>
"""

CONFIRM_CONTENT = """
<h1>Confirm Payment</h1>
<p class="info"><b>Number:</b> {{ number }}</p>
<p class="info"><b>Name:</b> {{ name }}</p>
<p class="info"><b>Provider:</b> {{ provider }}</p>
<p class="info"><b>Amount:</b> TSh {{ amount }}</p>
<p class="info"><b>Fee:</b> TSh {{ fee }}</p>
<p class="info total">Total: TSh {{ total }}</p>

<form method="post" action="/complete">
<input type="hidden" name="number" value="{{ number }}">
<input type="hidden" name="amount" value="{{ amount }}">
<input type="hidden" name="fee" value="{{ fee }}">
<button type="submit">Confirm Payment</button>
</form>
"""

SUCCESS_CONTENT = """
<h1>Payment Successful</h1>
<p class="info"><b>Number:</b> {{ number }}</p>
<p class="info"><b>Amount Sent:</b> TSh {{ amount }}</p>
<p class="info"><b>Fee:</b> TSh {{ fee }}</p>
<p class="info total">Total Deducted: TSh {{ total }}</p>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(
        BASE_TEMPLATE,
        title="ShenskoPay",
        content=HOME_CONTENT
    )

@app.route("/confirm", methods=["POST"])
def confirm():
    number = request.form["number"]
    amount = float(request.form["amount"])

    detected = detect_number(number) or {"name": "Pending verification", "provider": "Unknown"}

    fee = round(amount * FEE_PERCENTAGE, 2)
    total = amount + fee

    content = render_template_string(
        CONFIRM_CONTENT,
        number=number,
        name=detected["name"],
        provider=detected["provider"],
        amount=amount,
        fee=fee,
        total=total
    )

    return render_template_string(
        BASE_TEMPLATE,
        title="Confirm Payment",
        content=content
    )

@app.route("/complete", methods=["POST"])
def complete():
    number = request.form["number"]
    amount = float(request.form["amount"])
    fee = float(request.form["fee"])
    total = amount + fee

    content = render_template_string(
        SUCCESS_CONTENT,
        number=number,
        amount=amount,
        fee=fee,
        total=total
    )

    return render_template_string(
        BASE_TEMPLATE,
        title="Success",
        content=content
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
