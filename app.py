import os
from flask import Flask, request, render_template_string
from pesapal import create_payment  # your Pesapal integration
from detector import detect_number  # your number-to-name lookup

app = Flask(__name__)

FEE_PERCENTAGE = 0.01  # 1% transaction fee

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
input[type="text"], input[type="number"], select {
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
    <select name="payment_method" required>
        <option value="">Choose payment method</option>
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
<p>Amount: Tsh {{ amount }}</p>
<p>Transaction fee: Tsh {{ fee }}</p>
<p>Total: Tsh {{ total }}</p>
<p>Payment method: {{ method }}</p>
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
    method = request.form.get("payment_method")
    
    detected = detect_number(number)  # replace with real lookup
    name = detected["name"] if detected else "Unknown"
    provider = detected["provider"] if detected else "Unknown"
    
    fee = round(amount * FEE_PERCENTAGE, 2)
    total = amount + fee
    
    return render_template_string(confirm_template, number=number, name=name, provider=provider, amount=amount, fee=fee, total=total, method=method)

@app.route("/complete", methods=["POST"])
def complete():
    number = request.form.get("number")
    amount = float(request.form.get("amount"))
    fee = float(request.form.get("fee"))
    method = request.form.get("method")
    
    try:
        payment = create_payment(
            amount, 
            "TZS", 
            f"Payment to {number} via {method}", 
            os.environ.get("PESAPAL_CALLBACK_URL", "https://your-live-callback-url.com/complete")
        )
        redirect_url = payment.get("redirect_url", "No redirect URL received")
        return f"<div style='font-family:sans-serif; text-align:center; margin-top:50px;'><h2>Pesapal Payment Ready</h2><p>Click <a href='{redirect_url}' target='_blank'>here</a> to complete payment</p></div>"
    except Exception as e:
        return f"<div style='font-family:sans-serif; color:red; text-align:center; margin-top:50px;'><h2>Error</h2><p>{e}</p></div>", 500

if __name__ == "__main__":
    os.environ["PESAPAL_CONSUMER_KEY"] = os.environ.get("PESAPAL_CONSUMER_KEY", "YOUR_KEY")
    os.environ["PESAPAL_CONSUMER_SECRET"] = os.environ.get("PESAPAL_CONSUMER_SECRET", "YOUR_SECRET")
    app.run(host="0.0.0.0", port=5000, debug=True)
