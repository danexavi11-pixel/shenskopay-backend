from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShenskoPay</title>

    <style>
        * {
            box-sizing: border-box;
        }

        html, body {
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .box {
            background: #020617;
            padding: 20px;
            border-radius: 12px;
            width: 90%;
            max-width: 360px;
            text-align: center;
        }

        input, button {
            width: 100%;
            padding: 12px;
            margin-top: 12px;
            font-size: 16px;
            border-radius: 6px;
            border: none;
        }

        input {
            outline: none;
        }

        button {
            background: #22c55e;
            color: black;
            font-weight: bold;
            cursor: pointer;
        }

        #result {
            margin-top: 15px;
            font-size: 14px;
            word-wrap: break-word;
        }
    </style>
</head>
<body>
    <div class="box">
        <h2>ShenskoPay</h2>
        <input id="phone" placeholder="Enter phone number" />
        <button onclick="send()">Continue</button>
        <div id="result"></div>
    </div>

<script>
function send() {
    const phone = document.getElementById("phone").value;

    fetch("/detect", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ phone })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerText =
            JSON.stringify(data, null, 2);
    })
    .catch(() => {
        document.getElementById("result").innerText = "Error connecting to server";
    });
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/detect", methods=["POST"])
def detect():
    data = request.get_json()
    phone = data.get("phone") if data else None

    if not phone:
        return jsonify({"error": "Phone number required"}), 400

    return jsonify({
        "brand": "ShenskoPay",
        "phone": phone,
        "status": "READY_FOR_PAYMENT"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
