import os
import threading
from flask import Flask
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load token from environment variable (set via Replit Secrets)
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable not set")

# --- Minimal keep-alive web server (so Replit exposes a URL) ---
app_web = Flask("keep_alive")

@app_web.route("/")
def home():
    return "FreeCertify bot is alive!"

def run_web():
    # Replit will provide a port automatically via env (but Flask default 0.0.0.0:8080 works)
    app_web.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()

# --- Telegram bot handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to FreeCertify!\nType a topic (e.g., python, ai, web) and I'll fetch free courses."
    )

def get_static_courses(query):
    # Simple static fallback - you can expand with API calls later
    mapping = {
        "python": [
            "FreeCodeCamp: https://www.freecodecamp.org/learn/scientific-computing-with-python/",
            "Coursera: https://www.coursera.org/learn/python"
        ],
        "ai": [
            "Coursera: https://www.coursera.org/learn/ai-for-everyone",
            "FreeCodeCamp ML: https://www.freecodecamp.org/learn/machine-learning-with-python/"
        ]
    }
    return mapping.get(query.lower(), [])

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip().lower()
    results = get_static_courses(query)
    if results:
        await update.message.reply_text("\n\n".join(results))
        return

    # Example: call Coursera search API (basic)
    try:
        url = f"https://www.coursera.org/api/courses.v1?q=search&query={query}&limit=5"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            out = []
            for c in data.get("elements", [])[:5]:
                name = c.get("name")
                slug = c.get("slug")
                out.append(f"🎓 {name}\n🔗 https://www.coursera.org/learn/{slug}")
            if out:
                await update.message.reply_text("\n\n".join(out))
                return
    except Exception:
        pass

    await update.message.reply_text("❌ No free certified course found for that topic yet.")

# Robust run loop with retry on network errors
def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

    while True:
        try:
            print("✅ Bot started (polling)...")
            app.run_polling()
            break
        except Exception as e:
            print("Bot crashed / network error:", e)
            import time
            time.sleep(5)  # wait and retry

if __name__ == "__main__":
    # start the keep-alive web server
    keep_alive()
    # then start the bot (blocking)
    run_bot()
