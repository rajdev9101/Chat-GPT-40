from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import openai
import os
import threading

# Flask app for Koyeb health check
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "✅ Rajdev Bot is Alive with Flask + Telegram + OpenAI!"

# Telegram /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm Rajdev's AI bot. Ask me anything!")

# GPT message reply
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("⚠️ Error: " + str(e))

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

def run_telegram():
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    bot_token = os.environ.get("BOT_TOKEN")

    if not bot_token or not openai.api_key:
        print("❌ BOT_TOKEN or OPENAI_API_KEY not set!")
        return

    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_telegram()
