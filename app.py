import os
from flask import Flask, request, render_template_string
from detector import detect_number
from pesapal import create_payment

app = Flask(__name__)

FEE_PERCENTAGE = 0.013  # 1.3% transaction fee

home_template = """
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ShenskoPay</title>
<style>
body {
    margin: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #4a90e2, #50e3c2);
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}
.card {
    background: white;
    padding: 60px;
    border-radius: 25px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.25);
    width: 90%;
    max-width: 600px;
    text-align: center;
}
h2 {
    margin-bottom: 30px;
    font-size: 32px;
    color: #333;
}
input, select {
    width: 90%;
    padding: 18px;
    margin: 15px 0;
    border-radius: 12px;
    border: 1px solid #ccc;
    font-size: 18px;
}
button {
    padding: 16px 35px;
    background: #4a90e2;
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 18px;
    cursor: pointer;
}
</style>
</head>
<body>
<div class="card">
<h2>ShenskoPay</h2>
<form action="/confirm" method="post">
    <input type="text" name="number" placeholder="Enter recipient number" required>
    <input type="number" name="amount" placeholder="Enter amount (TZS)" required>
    <select name="method">
        <option value="auto">Choose payment method (Pesapal)</option>
    </select>
    <button type="submit">Continue</button>
</form>
</div>
</body>
</html>
"""

confirm_template = """
<!doctype html>
<html>
<body style="font-family:sans-serif; text-align:center; margin-top:60px;">
<h2>Confirm Payment</h2>
<p>Number: {{ number }}</p>
<p>Name: {{ name }}</p>
<p>Provider: {{ provider }}</p>
<p>Amount: {{ amount }}</p>
<p>Fee: {{ fee }}</p>
<p>Total: {{ total }}</p>
<form action="/complete" method="post">
<input type="hidden" name="number" value="{{ number }}">
<input type="hidden" name="amount" value="{{ amount }}">
<input type="hidden" name="fee" value="{{ fee }}">
<button type="submit">Pay Now</button>
</form>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(home_template)

@app.route("/confirm", methods=["POST"])
def confirm():
    number = request.form["number"]
    amount = float(request.form["amount"])
    detected = detect_number(number)
    name = detected["name"] if detected else "Unknown"
    provider = detected["provider"] if detected else "Unknown"
    fee = round(amount * FEE_PERCENTAGE, 2)
    total = amount + fee
    return render_template_string(
        confirm_template,
        number=number,
        name=name,
        provider=provider,
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

    payment = create_payment(
        total,
        f"ShenskoPay payment to {number}",
        "https://shenskopay-backend.onrender.com/callback"
    )

    return f"""
    <html>
    <body style="text-align:center; margin-top:60px;">
        <h2>Redirecting to payment…</h2>
        <script>
            window.location.href = "{payment['redirect_url']}";
        </script>
    </body>
    </html>
    """

@app.route("/callback")
def callback():
    return "<h2>Payment received. Processing…</h2>"

if __name__ == "__main__":
    app.run()
