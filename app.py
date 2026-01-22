from flask import Flask, request, render_template_string, redirect
from detector import detect_number
from pesapal import create_payment
import uuid

app = Flask(__name__)
FEE_PERCENTAGE = 0.01  # 1% fee per transaction

HTML_TEMPLATE = """ 
... [same premium card + background HTML as before] ...
"""

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

    # Generate unique reference
    reference = str(uuid.uuid4())

    # Description
    description = f"Payment to {number}"

    # Callback URL (Render public URL)
    callback_url = "https://your-render-url.onrender.com/callback"

    try:
        # Create real Pesapal payment
        payment_response = create_payment(reference, total, description, callback_url)
        payment_url = payment_response.get("payment_url")  # redirect user to Pesapal
        return redirect(payment_url)
    except Exception as e:
        return f"Payment error: {e}"

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
