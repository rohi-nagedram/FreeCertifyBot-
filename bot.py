import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Get your token from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set! Add it in Render Environment Variables.")

# Create Telegram bot app
application = ApplicationBuilder().token(BOT_TOKEN).build()

# --- Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Your bot is now running 24/7 on Render (Webhook Mode)!")

application.add_handler(CommandHandler("start", start))

# --- Flask Web Server ---
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is active.", 200

@app.route(f'/webhook/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.create_task(application.process_update(update))
    return "ok", 200

if __name__ == "__main__":
    # Local debug (Render auto-uses gunicorn)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
