from telebot import types

from config import (
    CHANNEL_USERNAME,
    CHANNEL_LINK
)


def is_joined(
    bot,
    user_id
):

    try:

        member = bot.get_chat_member(
            f"@{CHANNEL_USERNAME}",
            user_id
        )

        return member.status in [
            "member",
            "administrator",
            "creator"
        ]

    except:

        return False


def join_keyboard():

    markup = types.InlineKeyboardMarkup(
        row_width=2
    )

    markup.add(

        types.InlineKeyboardButton(
            "📢 Join Channel",
            url=CHANNEL_LINK
        ),

        types.InlineKeyboardButton(
            "✅ Verify",
            callback_data="verify_join"
        )

    )

    return markup


def send_join_required(
    bot,
    chat_id
):

    text = """
╔══════════════════════╗
      🔐 ACCESS REQUIRED
╚══════════════════════╝

📢 Join our official channel
before using this bot.

⚡ Verification required
🔒 Access protected

━━━━━━━━━━━━━━━━━━

👇 Join channel and press Verify
"""

    bot.send_message(
        chat_id,
        text,
        reply_markup=join_keyboard()
    )


def send_verified(
    bot,
    chat_id
):

    text = """
╔══════════════════════╗
      ✅ VERIFIED
╚══════════════════════╝

🎉 Channel membership verified.

🚀 All features unlocked.

Enjoy the bot.
"""

    bot.send_message(
        chat_id,
        text
    )
