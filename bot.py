import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Telegram Bot Token (from Render environment)
TOKEN = os.getenv("BOT_TOKEN")

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to *FreeCertify Bot!* 🎓\n"
        "I’ll send you free certification courses from trusted platforms.\n\n"
        "➡️ Type /courses to see what’s available!",
        parse_mode="Markdown"
    )

# Command: /courses
async def courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    free_courses = [
        ("FreeCodeCamp – Web Dev", "https://www.freecodecamp.org/learn/"),
        ("Google – Digital Marketing", "https://learndigital.withgoogle.com/digitalunlocked/"),
        ("Coursera – Free AI for Everyone", "https://www.coursera.org/learn/ai-for-everyone"),
        ("edX – Python Basics", "https://www.edx.org/learn/python")
    ]
    msg = "🎯 *Current Free Certification Courses:*\n\n"
    for name, link in free_courses:
        msg += f"✅ [{name}]({link})\n"
    await update.message.reply_text(msg, parse_mode="Markdown")

# Main app
if __name__ == "__main__":
    print("✅ Bot is running... (only free courses will be shown)")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("courses", courses))

    app.run_polling()
