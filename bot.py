from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

TOKEN = "8544023499:AAHX6jjFJuvd1KqG8-eUIZYnOMrM2XUdHks"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من Roxan هستم، می‌تونی با من چت کنی.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    # ارسال به API پابلیک Roxan
    url = "https://apifreellm.com/api/chat"
    data = {"message": user_msg}
    try:
        resp = requests.post(url, json=data, timeout=10)
        resp.raise_for_status()
        answer = resp.json().get("response", "هیچ جوابی دریافت نشد.")
    except Exception as e:
        answer = f"خطا در دریافت پاسخ! {str(e)}"

    await update.message.reply_text(answer)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
