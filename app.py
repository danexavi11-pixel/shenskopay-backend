from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>ShenskoPay</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .box {
            background: #020617;
            padding: 20px;
            border-radius: 10px;
            width: 300px;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
        }
        button {
            background: #22c55e;
            border: none;
            cursor: pointer;
        }
        #result {
            margin-top: 15px;
            font-size: 14px;
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
        body: JSON.stringify({phone})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerText =
            JSON.stringify(data, null, 2);
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
        "phone": phone,
        "network": "DETECTED",
        "next_step": "PAYMENT"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
