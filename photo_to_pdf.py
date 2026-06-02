from PIL import Image
import os

from config import (
    MENU,
    WAIT_PHOTOS,
    WAIT_PDF_NAME,
    MAX_PHOTOS
)

from utils.cleanup import (
    save_photo,
    get_all_photos,
    pdf_output_path,
    cleanup_user
)

from utils.stickers import (
    loading,
    processing,
    success,
    error
)

from utils.joincheck import (
    is_joined,
    send_join_required
)

from utils.keyboards import (
    main_menu,
    back_menu,
    create_pdf_keyboard,
    PHOTO_PROMPT,
    PDF_NAME_PROMPT,
    SUCCESS_MESSAGE,
    ERROR_MESSAGE,
    BACK_MESSAGE
)


def register_photo_to_pdf(
    bot,
    user_states,
    user_cache
):

    # =========================
    # OPEN PHOTO MODE
    # =========================

    @bot.message_handler(
        func=lambda m: m.text == "🖼 Photo ➜ PDF"
    )
    def photo_mode(message):

        chat_id = message.chat.id
        user_id = message.from_user.id

        loading(bot, chat_id)

        if not is_joined(bot, user_id):

            send_join_required(
                bot,
                chat_id
            )

            return

        cleanup_user(user_id)

        user_states[user_id] = WAIT_PHOTOS

        user_cache[user_id] = {
            "photos": 0
        }

        bot.send_message(
            chat_id,
            PHOTO_PROMPT,
            reply_markup=create_pdf_keyboard()
        )

    # =========================
    # RECEIVE PHOTOS
    # =========================

    @bot.message_handler(
        content_types=["photo"]
    )
    def receive_photo(message):

        user_id = message.from_user.id
        chat_id = message.chat.id

        if user_states.get(user_id) != WAIT_PHOTOS:
            return

        try:

            count = user_cache[user_id]["photos"]

            if count >= MAX_PHOTOS:

                bot.send_message(
                    chat_id,
                    f"❌ Maximum {MAX_PHOTOS} photos allowed."
                )

                return

            photo = message.photo[-1]

            file_info = bot.get_file(
                photo.file_id
            )

            downloaded = bot.download_file(
                file_info.file_path
            )

            save_photo(
                user_id,
                downloaded,
                count + 1
            )

            user_cache[user_id]["photos"] += 1

            loading(bot, chat_id)

            bot.reply_to(
                message,
                f"✅ Photo Saved ({count+1}/{MAX_PHOTOS})\n\nPress '✅ Create PDF' when finished."
            )

        except Exception as e:

            print(
                f"PHOTO SAVE ERROR: {e}"
            )

            error(
                bot,
                chat_id
            )

    # =========================
    # CREATE PDF BUTTON
    # =========================

    @bot.message_handler(
        func=lambda m: m.text == "✅ Create PDF"
    )
    def create_pdf(message):

        chat_id = message.chat.id
        user_id = message.from_user.id

        if user_states.get(user_id) != WAIT_PHOTOS:
            return

        total = user_cache.get(
            user_id,
            {}
        ).get(
            "photos",
            0
        )

        if total == 0:

            bot.send_message(
                chat_id,
                "❌ Send at least one photo."
            )

            return

        loading(
            bot,
            chat_id
        )

        user_states[user_id] = WAIT_PDF_NAME

        bot.send_message(
            chat_id,
            PDF_NAME_PROMPT,
            reply_markup=back_menu()
        )

    # =========================
    # RECEIVE PDF NAME
    # =========================

    @bot.message_handler(
        func=lambda m:
        user_states.get(
            m.from_user.id
        ) == WAIT_PDF_NAME
    )
    def receive_name(message):

        chat_id = message.chat.id
        user_id = message.from_user.id

        try:

            pdf_name = (
                message.text
                .strip()
                .replace(".pdf", "")
            )

            if len(pdf_name) < 1:

                bot.reply_to(
                    message,
                    "❌ Invalid file name."
                )

                return

            processing(
                bot,
                chat_id
            )

            photos = get_all_photos(
                user_id
            )

            images = []

            for photo in photos:

                img = Image.open(
                    photo
                ).convert(
                    "RGB"
                )

                images.append(
                    img
                )

            output_pdf = pdf_output_path(
                user_id,
                pdf_name
            )

            first = images[0]

            rest = images[1:]

            first.save(
                output_pdf,
                save_all=True,
                append_images=rest
            )

            with open(
                output_pdf,
                "rb"
            ) as pdf_file:

                bot.send_document(
                    chat_id,
                    pdf_file,
                    caption=
                    "📄 PDF Created Successfully\n\n❤️ Thanks for using Black Gold Converter."
                )

            success(
                bot,
                chat_id
            )

            bot.send_message(
                chat_id,
                SUCCESS_MESSAGE,
                reply_markup=main_menu()
            )

            cleanup_user(
                user_id
            )

            user_cache.pop(
                user_id,
                None
            )

            user_states[user_id] = MENU

        except Exception as e:

            print(
                f"PDF CREATE ERROR: {e}"
            )

            error(
                bot,
                chat_id
            )

            bot.send_message(
                chat_id,
                ERROR_MESSAGE
            )

            cleanup_user(
                user_id
            )

            user_states[user_id] = MENU

    # =========================
    # BACK BUTTON
    # =========================

    @bot.message_handler(
        func=lambda m:
        m.text == "🔙 Back"
    )
    def back_button(message):

        chat_id = message.chat.id
        user_id = message.from_user.id

        loading(
            bot,
            chat_id
        )

        cleanup_user(
            user_id
        )

        user_cache.pop(
            user_id,
            None
        )

        user_states[user_id] = MENU

        bot.send_message(
            chat_id,
            BACK_MESSAGE,
            reply_markup=main_menu()
        )
