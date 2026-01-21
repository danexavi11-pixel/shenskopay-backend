from flask import Flask, request, render_template_string
from detector import detect_number
from markupsafe import Markup

app = Flask(__name__)
FEE_PERCENTAGE = 0.01

BASE_HTML = """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ShenskoPay</title>

<style>
:root {
  --primary: #2563eb;
  --secondary: #0f172a;
  --bg: linear-gradient(135deg, #0f172a, #1e3a8a);
}

* { box-sizing: border-box; }

body {
  margin: 0;
  min-height: 100vh;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--bg);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.wrapper {
  width: 100%;
  max-width: 380px;
}

.brand {
  text-align: center;
  color: white;
  margin-bottom: 14px;
}

.brand h1 {
  margin: 0;
  font-size: 26px;
  letter-spacing: .5px;
}

.brand span {
  font-size: 13px;
  opacity: .85;
}

.card {
  background: white;
  border-radius: 18px;
  padding: 22px;
  box-shadow: 0 20px 40px rgba(0,0,0,.25);
  animation: fadeUp .4s ease;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

h2 {
  margin-top: 0;
  font-size: 18px;
  color: var(--secondary);
}

label {
  font-size: 13px;
  color: #475569;
}

input {
  width: 100%;
  padding: 12px 14px;
  margin-top: 6px;
  margin-bottom: 14px;
  font-size: 15px;
  border-radius: 12px;
  border: 1px solid #cbd5e1;
}

input:focus {
  outline: none;
  border-color: var(--primary);
}

button {
  width: 100%;
  padding: 14px;
  border: none;
  border-radius: 14px;
  font-size: 15px;
  font-weight: 600;
  background: var(--primary);
  color: white;
}

.info {
  font-size: 14px;
  color: #334155;
  margin: 6px 0;
}

.total {
  font-weight: 700;
  font-size: 16px;
  margin-top: 10px;
}

.footer {
  text-align: center;
  margin-top: 14px;
  font-size: 12px;
  color: #94a3b8;
}
</style>
</head>

<body>
<div class="wrapper">
  <div class="brand">
    <h1>ShenskoPay</h1>
    <span>Fast • Secure • Local</span>
  </div>

  <div class="card">
    {{ content }}
  </div>

  <div class="footer">© ShenskoPay</div>
</div>
</body>
</html>
"""

@app.route("/")
def home():
    content = Markup("""
    <h2>Send Money</h2>
    <form method="post" action="/confirm">
      <label>Recipient number</label>
      <input name="number" placeholder="07XXXXXXXX" required>

      <label>Amount (Tsh)</label>
      <input name="amount" type="number" placeholder="e.g. 2000" required>

      <button type="submit">Continue</button>
    </form>
    """)
    return render_template_string(BASE_HTML, content=content)

@app.route("/confirm", methods=["POST"])
def confirm():
    number = request.form["number"]
    amount = float(request.form["amount"])
    detected = detect_number(number) or {}
    fee = round(amount * FEE_PERCENTAGE, 2)
    total = amount + fee

    content = Markup(f"""
    <h2>Confirm Payment</h2>
    <div class="info"><b>To:</b> {detected.get("name", "Unknown")}</div>
    <div class="info"><b>Provider:</b> {detected.get("provider", "Unknown")}</div>
    <div class="info"><b>Amount:</b> Tsh {amount}</div>
    <div class="info"><b>Fee:</b> Tsh {fee}</div>
    <div class="total">Total: Tsh {total}</div>

    <form method="post" action="/complete">
      <input type="hidden" name="number" value="{number}">
      <input type="hidden" name="amount" value="{amount}">
      <input type="hidden" name="fee" value="{fee}">
      <button type="submit">Confirm & Pay</button>
    </form>
    """)
    return render_template_string(BASE_HTML, content=content)

@app.route("/complete", methods=["POST"])
def complete():
    number = request.form["number"]
    amount = float(request.form["amount"])
    fee = float(request.form["fee"])
    total = amount + fee

    content = Markup(f"""
    <h2>Payment Successful ✅</h2>
    <div class="info">Recipient: {number}</div>
    <div class="info">Amount sent: Tsh {amount}</div>
    <div class="info">Fee: Tsh {fee}</div>
    <div class="total">Total deducted: Tsh {total}</div>
    """)
    return render_template_string(BASE_HTML, content=content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
