from flask import Flask, request, redirect
from pesapal import create_payment

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return """
    <h2>ShenskoPay</h2>
    <form action="/pay" method="post">
        <input name="number" placeholder="Receiver number" required><br><br>
        <input name="amount" placeholder="Amount" type="number" required><br><br>
        <button type="submit">Continue</button>
    </form>
    """

@app.route("/pay", methods=["POST"])
def pay():
    number = request.form["number"]
    amount = request.form["amount"]

    callback_url = "https://shenskopay-backend.onrender.com/callback"

    payment = create_payment(
        amount=float(amount),
        currency="TZS",
        description=f"Send money to {number}",
        callback_url=callback_url
    )

    return redirect(payment["redirect_url"])


@app.route("/callback", methods=["GET"])
def callback():
    return "<h3>Payment received. Verification coming next.</h3>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
