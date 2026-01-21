from flask import Flask, request, render_template_string
from detector import detect_number
from pesapal import create_payment

app = Flask(__name__)

FEE_PERCENTAGE = 0.01  # 1% fee per transaction

# Home page template
home_template = """
<!doctype html>
<html>
<head>
<title>ShenskoPay</title>
<style>
body { font-family: Arial, sans-serif; display:flex; justify-content:center; align-items:center; height:100vh; background:#f0f2f5; }
.card { background:white; padding:30px; border-radius:10px; box-shadow:0 0 15px rgba(0,0,0,0.2); width:300px; text-align:center; }
input, button { width:100%; padding:10px; margin:10px 0; border-radius:5px; border:1px solid #ccc; }
button { background:#4CAF50; color:white; border:none; cursor:pointer; }
button:hover { background:#45a049; }
</style>
</head>
<body>
<div class="card">
<h2>ShenskoPay</h2>
<form action="{{ url_for('confirm') }}" method="post">
    <label>Enter number:</label><br>
    <input type="text" name="number" required><br>
    <label>Enter amount (Tsh):</label><br>
    <input type="number" name="amount" required><br>
    <button type="submit">Continue</button>
</form>
</div>
</body>
</html>
"""

# Confirm page template
confirm_template = """
<!doctype html>
<html>
<head>
<title>ShenskoPay - Confirm</title>
<style>
body { font-family: Arial, sans-serif; display:flex; justify-content:center; align-items:center; height:100vh; background:#f0f2f5; }
.card { background:white; padding:30px; border-radius:10px; box-shadow:0 0 15px rgba(0,0,0,0.2); width:350px; text-align:center; }
button { background:#4CAF50; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer; }
button:hover { background:#45a049; }
</style>
</head>
<body>
<div class="card">
<h2>Confirm Payment</h2>
<p>Number detected: {{ number }}</p>
<p>Name: {{ name }}</p>
<p>Provider: {{ provider }}</p>
<p>Amount: Tsh {{ amount }}</p>
<p>Transaction fee: Tsh {{ fee }}</p>
<p>Total to send: Tsh {{ total }}</p>
<form action="{{ url_for('complete') }}" method="post">
    <input type="hidden" name="number" value="{{ number }}">
    <input type="hidden" name="amount" value="{{ amount }}">
    <input type="hidden" name="fee" value="{{ fee }}">
    <button type="submit">Confirm Payment</button>
</form>
</div>
</body>
</html>
"""

# Success page template
success_template = """
<!doctype html>
<html>
<head>
<title>ShenskoPay - Success</title>
<style>
body { font-family: Arial, sans-serif; display:flex; justify-content:center; align-items:center; height:100vh; background:#f0f2f5; }
.card { background:white; padding:30px; border-radius:10px; box-shadow:0 0 15px rgba(0,0,0,0.2); width:350px; text-align:center; }
</style>
</head>
<body>
<div class="card">
<h2>Payment Successful ✅</h2>
<p>Number: {{ number }}</p>
<p>Amount Sent: Tsh {{ amount }}</p>
<p>Transaction Fee Collected: Tsh {{ fee }}</p>
<p>Total Deducted: Tsh {{ total }}</p>
{% if payment.url %}
<p><a href="{{ payment.url }}" target="_blank">Click here to pay via Pesapal</a></p>
{% elif payment.error %}
<p>Error: {{ payment.error }}</p>
{% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(home_template)

@app.route("/confirm", methods=["POST"])
def confirm():
    number = request.form.get("number")
    amount = float(request.form.get("amount"))
    
    detected = detect_number(number)
    if detected is None:
        name = "Unknown"
        provider = "Unknown"
    else:
        name = detected["name"]
        provider = detected["provider"]
    
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

    # Create real Pesapal payment
    payment_response = create_payment(
        amount=total,
        description=f"ShenskoPay payment to {number}",
        reference=f"SPAY-{number}",
        phone=number
    )

    return render_template_string(success_template,
                                  number=number,
                                  amount=amount,
                                  fee=fee,
                                  total=total,
                                  payment=payment_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
