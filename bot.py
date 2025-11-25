from flask import Flask, request, jsonify
from flask import Response

import requests

app = Flask(__name__)

# ===============================
# تابع چت Roxan با API پابلیک
# ===============================
def ask_roxan(prompt):
    url = "https://apifreellm.com/api/chat"
    data = {"message": prompt}
    resp = requests.post(url, json=data)
    result = resp.json()
    return result.get("response", "هیچ جوابی دریافت نشد.")

# ===============================
# مسیر اصلی صفحه HTML
# ===============================
@app.route("/")
def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Roxan Chat</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
                color: #fff;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .chat-container {
                background-color: rgba(0,0,0,0.6);
                width: 400px;
                max-width: 90%;
                border-radius: 10px;
                padding: 20px;
                display: flex;
                flex-direction: column;
            }
            #chat-box {
                flex: 1;
                overflow-y: auto;
                margin-bottom: 10px;
                padding: 10px;
                border: 1px solid #555;
                border-radius: 5px;
            }
            .message {
                margin: 5px 0;
            }
            .user {
                text-align: right;
                color: #4dd0e1;
            }
            .roxan {
                text-align: left;
                color: #ffcc80;
            }
            #user-input {
                padding: 10px;
                border-radius: 5px;
                border: none;
                width: calc(100% - 80px);
            }
            #send-btn {
                padding: 10px;
                margin-left: 5px;
                border: none;
                border-radius: 5px;
                background-color: #4dd0e1;
                color: #000;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div id="chat-box"></div>
            <input type="text" id="user-input" placeholder="پیام خود را اینجا تایپ کنید...">
            <button id="send-btn">ارسال</button>
        </div>
        <script>
            const sendBtn = document.getElementById("send-btn");
            const userInput = document.getElementById("user-input");
            const chatBox = document.getElementById("chat-box");

            sendBtn.addEventListener("click", sendMessage);
            userInput.addEventListener("keypress", function(e){
                if(e.key === "Enter") sendMessage();
            });

            function appendMessage(text, cls) {
                const msgDiv = document.createElement("div");
                msgDiv.classList.add("message", cls);
                msgDiv.textContent = text;
                chatBox.appendChild(msgDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            function sendMessage() {
                const msg = userInput.value.trim();
                if(msg === "") return;
                appendMessage(msg, "user");
                userInput.value = "";

                fetch("/ask", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({message: msg})
                })
                .then(res => res.json())
                .then(data => appendMessage(data.answer, "roxan"))
                .catch(err => appendMessage("خطا در دریافت پاسخ!", "roxan"));
            }
        </script>
    </body>
    </html>
    """
    return Response(html_content, mimetype='text/html')

# ===============================
# مسیر API برای پاسخ به پیام‌ها
# ===============================
@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message")
    answer = ask_roxan(user_input)
    return jsonify({"answer": answer})

# ===============================
# اجرا
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
