import os
import pypdfium2 as pdfium

from config import (
    MENU,
    WAIT_PDF,
    MAX_PDF_SIZE_MB
)

from utils.cleanup import (
    pdf_input_path,
    image_output_path,
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
    PDF_PROMPT,
    SUCCESS_MESSAGE,
    ERROR_MESSAGE,
    BACK_MESSAGE
)


def register_pdf_to_photo(
    bot,
    user_states
):

    # =========================
    # OPEN PDF MODE
    # =========================

    @bot.message_handler(
        func=lambda m: m.text == "📄 PDF ➜ Photo"
    )
    def pdf_mode(message):

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

        user_states[user_id] = WAIT_PDF

        bot.send_message(
            chat_id,
            PDF_PROMPT,
            reply_markup=back_menu()
        )

    # =========================
    # RECEIVE PDF
    # =========================

    @bot.message_handler(
        content_types=["document"]
    )
    def receive_pdf(message):

        user_id = message.from_user.id
        chat_id = message.chat.id

        if user_states.get(user_id) != WAIT_PDF:
            return

        try:

            if (
                message.document.mime_type
                != "application/pdf"
            ):

                error(
                    bot,
                    chat_id
                )

                bot.reply_to(
                    message,
                    "❌ Send a PDF file only."
                )

                return

            size_mb = (
                message.document.file_size
                / 1024
                / 1024
            )

            if size_mb > MAX_PDF_SIZE_MB:

                error(
                    bot,
                    chat_id
                )

                bot.reply_to(
                    message,
                    f"❌ PDF must be under {MAX_PDF_SIZE_MB} MB."
                )

                return

            processing(
                bot,
                chat_id
            )

            file_info = bot.get_file(
                message.document.file_id
            )

            downloaded = bot.download_file(
                file_info.file_path
            )

            pdf_path = pdf_input_path(
                user_id
            )

            with open(
                pdf_path,
                "wb"
            ) as f:

                f.write(
                    downloaded
                )

            # =====================
            # PDF -> IMAGES
            # =====================

            pdf = pdfium.PdfDocument(
                pdf_path
            )

            total_pages = len(pdf)

            for page_no in range(
                total_pages
            ):

                page = pdf[page_no]

                bitmap = page.render(
                    scale=2
                )

                pil_image = bitmap.to_pil()

                image_path = image_output_path(
                    user_id,
                    page_no + 1
                )

                pil_image.save(
                    image_path
                )

                with open(
                    image_path,
                    "rb"
                ) as img:

                    bot.send_photo(
                        chat_id,
                        img,
                        caption=(
                            f"📄 Page {page_no+1}/{total_pages}"
                        )
                    )

            pdf.close()

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

            user_states[user_id] = MENU

        except Exception as e:

            print(
                f"PDF2PHOTO ERROR: {e}"
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

        user_states[user_id] = MENU

        bot.send_message(
            chat_id,
            BACK_MESSAGE,
            reply_markup=main_menu()
        )
