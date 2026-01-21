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
body {
  margin: 0;
  font-family: system-ui, sans-serif;
  background: #eef2f7;
}
.wrapper {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
.card {
  background: white;
  width: 100%;
  max-width: 420px;
  padding: 24px;
  border-radius: 14px;
  box-shadow: 0 10px 25px rgba(0,0,0,.1);
}
h1 { text-align: center; }
input, button {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  margin-top: 12px;
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
<div class="wrapper">
<div class="card">
{{ content }}
</div>
</div>
</body>
</html>
"""

@app.route("/")
def home():
    content = Markup("""
    <h1>ShenskoPay</h1>
    <form method="post" action="/confirm">
      <input name="number" placeholder="Enter number" required>
      <input name="amount" type="number" placeholder="Amount (Tsh)" required>
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
    <h1>Confirm Payment</h1>
    <p><b>Number:</b> {number}</p>
    <p><b>Name:</b> {detected.get("name", "Unknown")}</p>
    <p><b>Provider:</b> {detected.get("provider", "Unknown")}</p>
    <p><b>Amount:</b> Tsh {amount}</p>
    <p><b>Fee:</b> Tsh {fee}</p>
    <p><b>Total:</b> Tsh {total}</p>
    <form method="post" action="/complete">
      <input type="hidden" name="number" value="{number}">
      <input type="hidden" name="amount" value="{amount}">
      <input type="hidden" name="fee" value="{fee}">
      <button type="submit">Confirm Payment</button>
    </form>
    """)

    return render_template_string(BASE_HTML, content=content)

@app.route("/complete", methods=["POST"])
def complete():
    amount = float(request.form["amount"])
    fee = float(request.form["fee"])
    total = amount + fee
    number = request.form["number"]

    content = Markup(f"""
    <h1>Payment Successful ✅</h1>
    <p>Number: {number}</p>
    <p>Total Deducted: Tsh {total}</p>
    """)

    return render_template_string(BASE_HTML, content=content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
