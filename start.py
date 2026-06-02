from config import (
    MENU
)

from utils.stickers import (
    loading,
    welcome,
    not_joined,
    error
)

from utils.joincheck import (
    is_joined,
    send_join_required
)

from utils.keyboards import (
    main_menu,
    MAIN_MENU_TEXT
)


def register_start(
    bot,
    user_states
):

    @bot.message_handler(
        commands=["start"]
    )
    def start_command(message):

        chat_id = message.chat.id
        user_id = message.from_user.id

        try:

            loading(
                bot,
                chat_id
            )

            if not is_joined(
                bot,
                user_id
            ):

                not_joined(
                    bot,
                    chat_id
                )

                send_join_required(
                    bot,
                    chat_id
                )

                return

            user_states[user_id] = MENU

            welcome(
                bot,
                chat_id
            )

            text = f"""
╔════════════════════════╗
      ⚡ BLACK GOLD ⚡
╚════════════════════════╝

👋 Welcome {message.from_user.first_name}

📄 PDF ➜ Photo
🖼 Photo ➜ PDF

🔒 Secure Conversion
⚡ Fast Processing
🚀 Premium Experience

━━━━━━━━━━━━━━━━━━

Select an option below 👇
"""

            bot.send_message(
                chat_id,
                text,
                reply_markup=main_menu()
            )

        except Exception as e:

            print(
                f"START ERROR: {e}"
            )

            error(
                bot,
                chat_id
            )
