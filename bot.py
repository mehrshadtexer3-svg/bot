from flask import Flask, request
from telegram import Bot, Update
import os
import requests

TOKEN = "8544023499:AAHX6jjFJuvd1KqG8-eUIZYnOMrM2XUdHks"
bot = Bot(token=TOKEN)

app = Flask(__name__)

# تابع پاسخ‌دهی Roxan (مثلاً همان API پابلیک یا Local LLM)
def ask_roxan(prompt):
    # نمونه ساده با API پابلیک
    url = "https://apifreellm.com/api/chat"
    try:
        resp = requests.post(url, json={"message": prompt}, timeout=10)
        resp.raise_for_status()
        return resp.json().get("response", "هیچ جوابی دریافت نشد.")
    except:
        return "خطا در دریافت پاسخ!"

# مسیر Webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    if update.message:
        chat_id = update.message.chat.id
        text = update.message.text
        answer = ask_roxan(text)
        bot.send_message(chat_id=chat_id, text=answer)
    return "ok"

# مسیر Health Check
@app.route("/")
def index():
    return "Roxan Bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
