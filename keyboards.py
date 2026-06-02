from telebot import types

from config import (
    OWNER_ID,
    CHANNEL_LINK,
    SUPPORT_LINK
)

# =========================
# MAIN MENU
# =========================

def main_menu():

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2
    )

    markup.add(
        "🖼 Photo ➜ PDF",
        "📄 PDF ➜ Photo"
    )

    markup.add(
        "💬 Support",
        "📢 Channel"
    )

    markup.add(
        "👑 Owner"
    )

    return markup


# =========================
# BACK MENU
# =========================

def back_menu():

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    markup.add(
        "🔙 Back"
    )

    return markup


# =========================
# CREATE PDF BUTTON
# =========================

def create_pdf_keyboard():

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    markup.add(
        "✅ Create PDF"
    )

    markup.add(
        "🔙 Back"
    )

    return markup


# =========================
# OWNER BUTTON
# =========================

def owner_keyboard():

    markup = types.InlineKeyboardMarkup()

    markup.add(

        types.InlineKeyboardButton(
            "👑 CONTACT OWNER",
            url=f"tg://user?id={OWNER_ID}"
        )

    )

    return markup


# =========================
# CHANNEL BUTTON
# =========================

def channel_keyboard():

    markup = types.InlineKeyboardMarkup()

    markup.add(

        types.InlineKeyboardButton(
            "📢 JOIN CHANNEL",
            url=CHANNEL_LINK
        )

    )

    return markup


# =========================
# SUPPORT BUTTON
# =========================

def support_keyboard():

    markup = types.InlineKeyboardMarkup()

    markup.add(

        types.InlineKeyboardButton(
            "💬 OPEN SUPPORT",
            url=SUPPORT_LINK
        )

    )

    return markup


# =========================
# TEXTS
# =========================

MAIN_MENU_TEXT = """
╔════════════════════════╗
        ⚡ BLACK GOLD ⚡
     PDF CONVERTER BOT
╚════════════════════════╝

🖼 Convert Photos ➜ PDF
📄 Convert PDF ➜ Photos

✨ Fast Processing
🔒 Secure Conversion
🚀 Premium Experience

━━━━━━━━━━━━━━━━━━

Choose an option below 👇
"""

PHOTO_PROMPT = """
╔════════════════════════╗
      🖼 PHOTO ➜ PDF
╚════════════════════════╝

📸 Send your photos.

✅ Up to 30 photos
✅ One PDF output
✅ HD quality

When finished press:

✔ CREATE PDF

━━━━━━━━━━━━━━━━━━
"""

PDF_NAME_PROMPT = """
╔════════════════════════╗
      📝 PDF FILE NAME
╚════════════════════════╝

Send a name for your PDF.

Example:

my_document

Output:

my_document.pdf
"""

PDF_PROMPT = """
╔════════════════════════╗
      📄 PDF ➜ PHOTO
╚════════════════════════╝

📤 Send your PDF file.

✅ All pages supported
✅ HD image output
✅ Fast processing
"""

SUCCESS_MESSAGE = """
╔════════════════════════╗
     ✅ CONVERSION DONE
╚════════════════════════╝

🎉 Your file is ready.

❤️ Thanks for using
Black Gold Converter.

📢 Join our channel
for updates.

🚀 Use again anytime.
"""

ERROR_MESSAGE = """
╔════════════════════════╗
      ❌ FAILED
╚════════════════════════╝

Something went wrong.

🔄 Please try again.
"""

BACK_MESSAGE = """
🔙 Back to Main Menu

Choose an option below 👇
"""
