import os
import threading

from flask import Flask

import telebot

from config import (
    BOT_TOKEN
)

# =========================
# BOT
# =========================

bot = telebot.TeleBot(
    BOT_TOKEN,
    parse_mode="HTML",
    threaded=True
)

# =========================
# FLASK
# =========================

app = Flask(__name__)

# =========================
# STATES
# =========================

user_states = {}
user_cache = {}

# =========================
# IMPORT HANDLERS
# =========================

from handlers.start import (
    register_start
)

from handlers.callbacks import (
    register_callbacks
)

from handlers.photo_to_pdf import (
    register_photo_to_pdf
)

from handlers.pdf_to_photo import (
    register_pdf_to_photo
)

# =========================
# REGISTER
# =========================

register_start(
    bot,
    user_states
)

register_callbacks(
    bot,
    user_states
)

register_photo_to_pdf(
    bot,
    user_states,
    user_cache
)

register_pdf_to_photo(
    bot,
    user_states
)

# =========================
# HEALTH ROUTE
# =========================

@app.route("/")
def home():
    return "Black Gold PDF Bot Running", 200   # FIX: tuple issue fixed

# =========================
# START POLLING
# =========================

def run_bot():
    print("Bot Started...")

    bot.infinity_polling(
        skip_pending=True,
        timeout=30,
        long_polling_timeout=30
    )

# =========================
# MAIN
# =========================

if __name__ == "__main__":

    # FIX 1: ensure bot token exists
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is missing in environment variables")

    # FIX 2: safer thread handling
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True   # important fix for Render/Railway
    bot_thread.start()

    # FIX 3: Render safe port binding
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
)
