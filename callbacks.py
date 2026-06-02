from config import (
    MENU
)

from utils.stickers import (
    loading,
    welcome,
    success,
    error
)

from utils.joincheck import (
    is_joined,
    send_join_required,
    send_verified
)

from utils.keyboards import (
    main_menu
)


def register_callbacks(
    bot,
    user_states
):

    @bot.callback_query_handler(
        func=lambda call: True
    )
    def callback_handler(call):

        chat_id = call.message.chat.id
        user_id = call.from_user.id

        try:

            # =========================
            # VERIFY JOIN
            # =========================

            if call.data == "verify_join":

                loading(
                    bot,
                    chat_id
                )

                if not is_joined(
                    bot,
                    user_id
                ):

                    error(
                        bot,
                        chat_id
                    )

                    bot.answer_callback_query(
                        call.id,
                        "❌ Join channel first",
                        show_alert=True
                    )

                    return

                user_states[user_id] = MENU

                success(
                    bot,
                    chat_id
                )

                welcome(
                    bot,
                    chat_id
                )

                try:

                    bot.delete_message(
                        chat_id,
                        call.message.message_id
                    )

                except:
                    pass

                send_verified(
                    bot,
                    chat_id
                )

                text = f"""
╔════════════════════════╗
      ⚡ BLACK GOLD ⚡
╚════════════════════════╝

🎉 Verification Successful

📄 PDF ➜ Photo
🖼 Photo ➜ PDF

⚡ Fast
🔒 Secure
🚀 Premium

━━━━━━━━━━━━━━━━━━

Choose an option below 👇
"""

                bot.send_message(
                    chat_id,
                    text,
                    reply_markup=main_menu()
                )

                bot.answer_callback_query(
                    call.id,
                    "✅ Verified"
                )

        except Exception as e:

            print(
                f"CALLBACK ERROR: {e}"
            )

            error(
                bot,
                chat_id
            )

            try:

                bot.answer_callback_query(
                    call.id,
                    "❌ Error"
                )

            except:
                pass
