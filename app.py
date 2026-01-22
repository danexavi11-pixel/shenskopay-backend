from flask import Flask, request, render_template_string
from detector import detect_number

app = Flask(__name__)
FEE_PERCENTAGE = 0.01  # 1% fee per transaction

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
<title>ShenskoPay</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
html,body{height:100%;font-family:'Segoe UI',Roboto,sans-serif;overflow-x:hidden;}

body{
  display:flex;justify-content:center;align-items:center;
  min-height:100vh;
  background: linear-gradient(135deg,#0b1d38,#1a2b4c);
  position:relative;
}

/* Branded Watermark Background */
body::before{
  content:'';
  position:absolute;top:0;left:0;width:100%;height:100%;
  background:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="500" height="120"><text x="0" y="70" font-family="Verdana" font-size="70" fill="rgba(255,111,0,0.05)" transform="rotate(-25 0 50)">ShenskoPay</text></svg>') repeat;
  z-index:0;pointer-events:none;
  animation:moveWatermark 60s linear infinite;
}
@keyframes moveWatermark{
  0%{background-position:0 0;}
  100%{background-position:800px 600px;}
}

/* Premium Card */
.card{
  width:90%; max-width:850px;
  background: rgba(255,255,255,0.97);
  border-radius:32px;
  padding:60px;
  box-shadow:0 25px 70px rgba(0,0,0,0.6);
  position:relative;
  z-index:1;
  text-align:center;
  transition:0.3s;
}
.card:hover{transform:scale(1.02);}
.brand{font-size:72px;font-weight:900;color:#ff6f00;margin-bottom:12px;text-shadow:2px 2px 5px rgba(0,0,0,0.3);}
.tagline{font-size:24px;color:#444;margin-bottom:40px;}

label{display:block;font-weight:700;font-size:20px;color:#222;margin-bottom:10px;text-align:left;}
input{width:100%;padding:20px;margin-bottom:24px;border-radius:16px;border:1px solid #ccc;font-size:22px;transition:0.3s;}
input:focus{outline:none;border-color:#ff6f00;transform:scale(1.02);}

button{
  width:100%;padding:20px;font-size:26px;font-weight:900;border:none;border-radius:16px;
  background:linear-gradient(135deg,#ff6f00,#ffb300);
  color:white;cursor:pointer;transition:0.3s;
}
button:hover{transform:translateY(-3px) scale(1.02);box-shadow:0 15px 35px rgba(0,0,0,0.5);}

.info{font-size:22px;margin:14px 0;}
.total{margin-top:18px;font-size:28px;font-weight:900;}
.success{font-size:36px;font-weight:900;color:#2e7d32;margin-top:20px;}

@media(max-width:600px){
  .card{padding:32px;}
  .brand{font-size:52px;}
  .tagline{font-size:20px;}
  input{padding:16px;font-size:20px;}
  button{padding:16px;font-size:22px;}
}
</style>
</head>
<body>
<div class="card">
<div class="brand">💰 ShenskoPay</div>
<div class="tagline">Fast • Secure • Trusted Payments</div>

<form action="/confirm" method="post">
<label>Recipient Number</label>
<input name="number" placeholder="07XXXXXXXX" required>
<label>Amount (TZS)</label>
<input type="number" name="amount" placeholder="Enter amount" required>
<button type="submit">Continue</button>
</form>

{% if number %}
<div class="info">Number: {{ number }}</div>
<div class="info">Name: {{ name }}</div>
<div class="info">Provider: {{ provider }}</div>
<div class="info">Amount: Tsh {{ amount }}</div>
<div class="info">Transaction Fee: Tsh {{ fee }}</div>
<div class="total">Total to send: Tsh {{ total }}</div>
<form action="/complete" method="post">
<input type="hidden" name="number" value="{{ number }}">
<input type="hidden" name="amount" value="{{ amount }}">
<input type="hidden" name="fee" value="{{ fee }}">
<button type="submit">Confirm Payment</button>
</form>
{% endif %}

{% if success %}
<div class="success">Payment Successful ✅</div>
<div class="info">Number: {{ number }}</div>
<div class="info">Amount Sent: Tsh {{ amount }}</div>
<div class="info">Fee Collected: Tsh {{ fee }}</div>
<div class="info">Total Deducted: Tsh {{ total }}</div>
{% endif %}

</div>
</body>
</html>
"""

from flask import render_template_string

@app.route("/", methods=["GET"])
def home(): return render_template_string(HTML_TEMPLATE)

@app.route("/confirm", methods=["POST"])
def confirm():
    number = request.form["number"]
    amount = float(request.form["amount"])
    detected = detect_number(number)
    fee = round(amount*FEE_PERCENTAGE,2)
    total = amount+fee
    return render_template_string(HTML_TEMPLATE,
                                  number=number,
                                  name=detected["name"] if detected else "Unknown",
                                  provider=detected["provider"] if detected else "Unknown",
                                  amount=amount,
                                  fee=fee,
                                  total=total)

@app.route("/complete", methods=["POST"])
def complete():
    number = request.form["number"]
    amount = float(request.form["amount"])
    fee = float(request.form["fee"])
    total = amount+fee
    return render_template_string(HTML_TEMPLATE,
                                  success=True,
                                  number=number,
                                  amount=amount,
                                  fee=fee,
                                  total=total)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
