from flask import Flask, request, render_template_string

app = Flask(__name__)

# 1.3% transaction fee
FEE_PERCENTAGE = 0.013


# --------- TEMP SAFE DETECTOR (NO UNKNOWN) ----------
def detect_number(number):
    # Simple placeholder logic (replace later with telco APIs)
    providers = {
        "075": ("Vodacom", "M-Pesa User"),
        "076": ("Vodacom", "M-Pesa User"),
        "074": ("Vodacom", "M-Pesa User"),
        "071": ("Airtel", "Airtel Money User"),
        "068": ("Airtel", "Airtel Money User"),
        "065": ("Tigo", "Tigo Pesa User"),
        "067": ("Tigo", "Tigo Pesa User"),
        "062": ("Halotel", "Halopesa User"),
    }
    prefix = number[:3]
    if prefix in providers:
        provider, name = providers[prefix]
        return {"provider": provider, "name": name}
    return {"provider": "Mobile Network", "name": "Registered User"}
# ----------------------------------------------------


home_template = """
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ShenskoPay</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #4a90e2, #50e3c2);
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.container {
    transition: transform 0.3s ease;
}

.container.focused {
    transform: translateY(-40px);
}

.card {
    background: white;
    padding: 60px;
    border-radius: 26px;
    box-shadow: 0 18px 40px rgba(0,0,0,0.25);
    width: 92%;
    max-width: 620px;
    text-align: center;
}

h2 {
    margin-bottom: 35px;
    font-size: 34px;
    color: #222;
}

input, select {
    width: 100%;
    padding: 20px;
    margin: 16px 0;
    border-radius: 14px;
    border: 1.5px solid #ccc;
    font-size: 20px;
}

input:focus, select:focus {
    outline: none;
    border-color: #4a90e2;
}

button {
    margin-top: 25px;
    padding: 18px;
    width: 100%;
    background: #4a90e2;
    color: white;
    border: none;
    border-radius: 14px;
    font-size: 20px;
    cursor: pointer;
}

button:hover {
    background: #357ABD;
}

.background-text {
    position: absolute;
    top: 20px;
    left: 20px;
    font-size: 64px;
    font-weight: bold;
    color: rgba(255,255,255,0.15);
}
</style>

<script>
document.addEventListener("DOMContentLoaded", () => {
    const inputs = document.querySelectorAll("input, select");
    const container = document.querySelector(".container");

    inputs.forEach(el => {
        el.addEventListener("focus", () => container.classList.add("focused"));
        el.addEventListener("blur", () => container.classList.remove("focused"));
    });
});
</script>

</head>
<body>

<div class="background-text">SHENSKOPAY</div>

<div class="container">
    <div class="card">
        <h2>ShenskoPay</h2>
        <form action="/confirm" method="post">
            <input type="text" name="number" placeholder="Enter recipient number" required>
            <input type="number" name="amount" placeholder="Enter amount (TZS)" required>

            <select name="method" required>
                <option value="mobile_money">Mobile Money</option>
                <option value="bank">Bank</option>
                <option value="card">Card</option>
            </select>

            <button type="submit">Continue</button>
        </form>
    </div>
</div>

</body>
</html>
"""


confirm_template = """
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Confirm Payment</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {
    margin:0;
    font-family:'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #4a90e2, #50e3c2);
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
}
.card {
    background:white;
    padding:55px;
    border-radius:26px;
    width:92%;
    max-width:620px;
    box-shadow:0 18px 40px rgba(0,0,0,0.25);
}
p {
    font-size:21px;
    margin:14px 0;
}
button {
    margin-top:25px;
    width:100%;
    padding:18px;
    font-size:20px;
    background:#4a90e2;
    color:white;
    border:none;
    border-radius:14px;
}
</style>
</head>
<body>

<div class="card">
<h2>Confirm Payment</h2>
<p><b>Name:</b> {{ name }}</p>
<p><b>Number:</b> {{ number }}</p>
<p><b>Provider:</b> {{ provider }}</p>
<p><b>Method:</b> {{ method }}</p>
<p><b>Amount:</b> TZS {{ amount }}</p>
<p><b>Fee (1.3%):</b> TZS {{ fee }}</p>
<p><b>Total:</b> TZS {{ total }}</p>

<form action="/complete" method="post">
    <input type="hidden" name="number" value="{{ number }}">
    <input type="hidden" name="total" value="{{ total }}">
    <button type="submit">Confirm Payment</button>
</form>
</div>

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
    method = request.form["method"]

    detected = detect_number(number)
    fee = round(amount * FEE_PERCENTAGE, 2)
    total = amount + fee

    return render_template_string(
        confirm_template,
        number=number,
        name=detected["name"],
        provider=detected["provider"],
        method=method,
        amount=amount,
        fee=fee,
        total=total
    )


@app.route("/complete", methods=["POST"])
def complete():
    return "<h2 style='text-align:center;font-family:sans-serif;margin-top:60px;'>Payment flow ready (Pesapal next)</h2>"


if __name__ == "__main__":
    app.run()
