from flask import Flask, request, render_template_string
from detector import detect_number

app = Flask(__name__)

FEE_PERCENTAGE = 0.01  # 1%

BASE_HTML = """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ShenskoPay</title>
<style>
* {
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}

body {
  margin: 0;
  min-height: 100vh;
  background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
  display: flex;
  justify-content: center;
  align-items: center;
}

.card {
  background: white;
  width: 100%;
  max-width: 420px;
  padding: 24px;
  border-radius: 18px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.25);
}

.brand {
  text-align: center;
  font-size: 28px;
  font-weight: 700;
  color: #203a43;
  margin-bottom: 20px;
}

label {
  font-size: 14px;
  color: #444;
}

input {
  width: 100%;
  padding: 14px;
  margin-top: 6px;
  margin-bottom: 16px;
  border-radius: 12px;
  border: 1px solid #ccc;
  font-size: 16px;
}

button {
  width: 100%;
  padding: 14px;
  border: none;
  border-radius: 14px;
  background: #203a43;
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

button:hover {
  background: #1b2f38;
}

.row {
  margin-bottom: 10px;
  font-size: 15px;
}

.total {
  font-weight: bold;
  font-size: 17px;
  margin-top: 10px;
}
</style>
</head>
<body>
<div class="card">
{{ content }}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    content = """
    <div class="brand">ShenskoPay</div>
    <form method="post" action="/confirm">
      <label>Recipient Number</label>
      <input name="number" required>

      <label>Amount (Tsh)</label>
      <input type="number" name="amount" required>

      <button>Continue</button>
    </form>
    """
    return render_template_string(BASE_HTML, content=content)

@app.route("/confirm", methods=["POST"])
def confirm():
    number = request.form["number"]
    amount = float(request.form["amount"])

    detected = detect_number(number)
    name = detected["name"] if detected else "Unknown"
    provider = detected["provider"] if detected else "Unknown"

    fee = round(amount * FEE_PERCENTAGE, 2)
    total = amount + fee

    content = f"""
    <div class="brand">Confirm Payment</div>
    <div class="row">Recipient: <b>{name}</b></div>
    <div class="row">Provider: {provider}</div>
    <div class="row">Amount: Tsh {amount}</div>
    <div class="row">Fee: Tsh {fee}</div>
    <div class="row total">Total: Tsh {total}</div>

    <form method="post" action="/complete">
      <input type="hidden" name="number" value="{number}">
      <input type="hidden" name="amount" value="{amount}">
      <input type="hidden" name="fee" value="{fee}">
      <button>Confirm Payment</button>
    </form>
    """
    return render_template_string(BASE_HTML, content=content)

@app.route("/complete", methods=["POST"])
def complete():
    content = """
    <div class="brand">Success ✅</div>
    <div class="row">Payment initiated.</div>
    <div class="row">This is a demo flow.</div>
    """
    return render_template_string(BASE_HTML, content=content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
