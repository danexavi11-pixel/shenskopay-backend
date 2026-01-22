import os
from flask import Flask, request, render_template_string
from detector import detect_number  # placeholder, implement later
from pesapal import create_payment   # placeholder, implement later

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
input[type="text"], input[type="number"] {
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
    transition: 0.3s;
}
button:hover {
    background: #357ABD;
}
select {
    padding:12px; font-size:16px; margin:12px 0; border-radius:12px;
}
.background-text {
    position: absolute;
    top: 20px;
    left: 20px;
    font-size: 60px;
    font-weight: bold;
    color: rgba(255,255,255,0.15);
    z-index: 0;
}
</style>
</head>
<body>
<div class="background-text">SHENSKOPAY</div>
<div class="card">
<h2>ShenskoPay</h2>
<form action="{{ url_for('confirm') }}" method="post">
    <input type="text" name="number" placeholder="Enter recipient number" required><br>
    <input type="number" name="amount" placeholder="Enter amount (Tsh)" required><br>
    <label for="method">Choose payment method:</label><br>
    <select name="method" id="method">
        <option value="mobile_money">Mobile Money</option>
        <option value="bank">Bank</option>
        <option value="card">Card</option>
    </select><br>
    <button type="submit">Continue</button>
</form>
</div>
</body>
</html>
"""

confirm_template = """
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ShenskoPay - Confirm</title>
<style>
body { margin:0; font-family:'Segoe UI',sans-serif; background:linear-gradient(135deg, #4a90e2, #50e3c2); display:flex; justify-content:center; align-items:center; height:100vh; }
.card { background:white; padding:50px; border-radius:25px; box-shadow:0 15px 35px rgba(0,0,0,0.25); width:90%; max-width:600px; text-align:center; }
p { font-size:20px; margin:12px 0; color:#333; }
button { padding:16px 35px; background:#4a90e2; color:white; border:none; border-radius:12px; font-size:18px; cursor:pointer; transition:0.3s; margin-top:15px; }
button:hover { background:#357ABD; }
</style>
</head>
<body>
<div class="card">
<h2>Confirm Payment</h2>
<p>Number: {{ number }}</p>
<p>Name: {{ name }}</p>
<p>Provider: {{ provider }}</p>
<p>Payment Method: {{ method }}</p>
<p>Amount: Tsh {{ amount }}</p>
<p>Transaction fee: Tsh {{ fee }}</p>
<p>Total: Tsh {{ total }}</p>
<form action="{{ url_for('complete') }}" method="post">
    <input type="hidden" name="number" value="{{ number }}">
    <input type="hidden" name="amount" value="{{ amount }}">
    <input type="hidden" name="fee" value="{{ fee }}">
    <input type="hidden" name="method" value="{{ method }}">
    <button type="submit">Confirm Payment</button>
</form>
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
    method = request.form.get("method")
    detected = detect_number(number)
    name = detected["name"] if detected else "Unknown"
    provider = detected["provider"] if detected else "Unknown"
    fee = round(amount * FEE_PERCENTAGE,2)
    total = amount + fee
    return render_template_string(confirm_template, number=number, name=name, provider=provider, method=method, amount=amount, fee=fee, total=total)

@app.route("/complete", methods=["POST"])
def complete():
    number = request.form.get("number")
    amount = float(request.form.get("amount"))
    fee = float(request.form.get("fee"))
    method = request.form.get("method")
    total = amount + fee
    # Placeholder for Pesapal integration
    return f"<div style='font-family:sans-serif; text-align:center; margin-top:50px;'><h2>Payment Ready</h2><p>Method: {method}</p><p>Number: {number}</p><p>Total: Tsh {total}</p><p>(Integration with Pesapal to be done)</p></div>"

if __name__ == "__main__":
    app.run(debug=True)
