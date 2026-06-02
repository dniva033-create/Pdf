import time
import threading

from config import (
    STICKER_LOADING,
    STICKER_WELCOME,
    STICKER_NOT_JOINED,
    STICKER_ERROR,
    STICKER_SUCCESS,
    STICKER_PROCESSING
)


DELETE_AFTER = 0.6


def _delete_later(
    bot,
    chat_id,
    message_id
):

    try:

        time.sleep(
            DELETE_AFTER
        )

        bot.delete_message(
            chat_id,
            message_id
        )

    except:
        pass


def _send(
    bot,
    chat_id,
    sticker_id
):

    try:

        msg = bot.send_sticker(
            chat_id,
            sticker_id
        )

        threading.Thread(
            target=_delete_later,
            args=(
                bot,
                chat_id,
                msg.message_id
            ),
            daemon=True
        ).start()

    except:
        pass


# =========================
# PUBLIC FUNCTIONS
# =========================

def loading(
    bot,
    chat_id
):

    _send(
        bot,
        chat_id,
        STICKER_LOADING
    )


def welcome(
    bot,
    chat_id
):

    _send(
        bot,
        chat_id,
        STICKER_WELCOME
    )


def not_joined(
    bot,
    chat_id
):

    _send(
        bot,
        chat_id,
        STICKER_NOT_JOINED
    )


def processing(
    bot,
    chat_id
):

    _send(
        bot,
        chat_id,
        STICKER_PROCESSING
    )


def success(
    bot,
    chat_id
):

    _send(
        bot,
        chat_id,
        STICKER_SUCCESS
    )


def error(
    bot,
    chat_id
):

    _send(
        bot,
        chat_id,
        STICKER_ERROR
    )
