from flask import Flask, request, render_template_string, redirect, url_for
from detector import detect_number

app = Flask(__name__)

FEE_PERCENTAGE = 0.01  # 1% fee per transaction

# --- HTML Templates ---
home_template = """
<!doctype html>
<html>
<head>
    <title>ShenskoPay</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 0 15px rgba(0,0,0,0.2); width: 300px; text-align: center; }
        input { width: 90%; padding: 10px; margin: 10px 0; border-radius: 5px; border: 1px solid #ccc; }
        button { padding: 10px 20px; border: none; background: #007bff; color: white; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h2>ShenskoPay</h2>
        <form action="{{ url_for('confirm') }}" method="post">
            <input type="text" name="number" placeholder="Enter number" required><br>
            <input type="number" name="amount" placeholder="Amount (Tsh)" required><br>
            <button type="submit">Continue</button>
        </form>
    </div>
</body>
</html>
"""

confirm_template = """
<!doctype html>
<html>
<head>
    <title>ShenskoPay - Confirm</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 15px rgba(0,0,0,0.2); width: 350px; text-align: center; }
        p { margin: 10px 0; }
        button { padding: 10px 20px; border: none; background: #28a745; color: white; border-radius: 5px; cursor: pointer; margin-top: 15px; }
        button:hover { background: #218838; }
    </style>
</head>
<body>
    <div class="container">
        <h2>ShenskoPay</h2>
        <p><strong>Number detected:</strong> {{ number }}</p>
        <p><strong>Name:</strong> {{ name }}</p>
        <p><strong>Provider:</strong> {{ provider }}</p>
        <p><strong>Amount:</strong> Tsh {{ amount }}</p>
        <p><strong>Transaction fee:</strong> Tsh {{ fee }}</p>
        <p><strong>Total to send:</strong> Tsh {{ total }}</p>
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
<html>
<head>
    <title>ShenskoPay - Success</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 15px rgba(0,0,0,0.2); width: 350px; text-align: center; }
        p { margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Payment Successful ✅</h2>
        <p><strong>Number:</strong> {{ number }}</p>
        <p><strong>Amount Sent:</strong> Tsh {{ amount }}</p>
        <p><strong>Transaction Fee Collected:</strong> Tsh {{ fee }}</p>
        <p><strong>Total Deducted:</strong> Tsh {{ total }}</p>
    </div>
</body>
</html>
"""

# --- Routes ---
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

    # Payment gateway integration will go here later

    return render_template_string(success_template,
                                  number=number,
                                  amount=amount,
                                  fee=fee,
                                  total=total)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
