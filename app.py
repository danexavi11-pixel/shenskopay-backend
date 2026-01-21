from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

FEE_PERCENTAGE = 0.01  # 1% fee per transaction

def detect_number(value: str):
    value = value.strip()
    # TZ mobile numbers
    if re.fullmatch(r"(0|255)[67]\d{8}", value):
        return {"provider": "Vodacom/Tigo/Airtel/Halotel/Mantel/TTCL", "name": "James Mwita"}
    # Control numbers (gov / bills)
    if re.fullmatch(r"\d{10,15}", value):
        return {"provider": "Government", "name": "TRA Payment"}
    # Merchant / Lipa Namba
    if re.fullmatch(r"\d{5,7}", value):
        return {"provider": "Merchant", "name": "ABC Store"}
    # Bank account
    if re.fullmatch(r"\d{8,16}", value):
        return {"provider": "Bank", "name": "CRDB Account"}
    return None

home_template = """
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ShenskoPay</title>
<style>
body {
    margin: 0; 
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #f6d365, #fda085);
    display: flex; 
    justify-content: center; 
    align-items: center; 
    height: 100vh;
}
.card {
    background: white;
    padding: 40px 50px;
    border-radius: 15px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    width: 100%;
    max-width: 400px;
    text-align: center;
}
h2 { margin-bottom: 30px; color: #ff6f61; }
input[type=text], input[type=number] {
    width: 100%;
    padding: 12px 15px;
    margin: 8px 0 20px 0;
    border: 1px solid #ccc;
    border-radius: 10px;
    box-sizing: border-box;
    font-size: 16px;
}
button {
    background-color: #ff6f61;
    color: white;
    padding: 14px 0;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    width: 100%;
    font-size: 18px;
}
button:hover { background-color: #ff3b2e; }
</style>
</head>
<body>
<div class="card">
<h2>ShenskoPay</h2>
<form action="{{ url_for('confirm') }}" method="post">
<label>Enter number:</label>
<input type="text" name="number" required>
<label>Enter amount (Tsh):</label>
<input type="number" name="amount" required>
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
body { margin: 0; font-family: Arial, sans-serif; background: linear-gradient(135deg, #f6d365, #fda085); display: flex; justify-content: center; align-items: center; height: 100vh; }
.card { background: white; padding: 40px 50px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); width: 100%; max-width: 400px; text-align: center; }
h2 { margin-bottom: 20px; color: #ff6f61; }
p { font-size: 18px; margin: 10px 0; }
button { background-color: #ff6f61; color: white; padding: 14px 0; border: none; border-radius: 10px; cursor: pointer; width: 100%; font-size: 18px; margin-top: 20px; }
button:hover { background-color: #ff3b2e; }
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

success_template = """
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ShenskoPay - Success</title>
<style>
body { margin: 0; font-family: Arial, sans-serif; background: linear-gradient(135deg, #f6d365, #fda085); display: flex; justify-content: center; align-items: center; height: 100vh; }
.card { background: white; padding: 40px 50px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); width: 100%; max-width: 400px; text-align: center; }
h2 { margin-bottom: 20px; color: #28a745; }
p { font-size: 18px; margin: 10px 0; }
</style>
</head>
<body>
<div class="card">
<h2>Payment Successful ✅</h2>
<p>Number: {{ number }}</p>
<p>Amount Sent: Tsh {{ amount }}</p>
<p>Transaction Fee Collected: Tsh {{ fee }}</p>
<p>Total Deducted: Tsh {{ total }}</p>
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
    name = detected["name"] if detected else "Unknown"
    provider = detected["provider"] if detected else "Unknown"
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
    # Real payment gateway integration comes later
    return render_template_string(success_template,
                                  number=number,
                                  amount=amount,
                                  fee=fee,
                                  total=total)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
