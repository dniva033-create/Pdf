import os
import shutil


BASE_TEMP = "temp"


def ensure_temp():

    os.makedirs(
        BASE_TEMP,
        exist_ok=True
    )


def get_user_folder(
    user_id
):

    ensure_temp()

    folder = os.path.join(
        BASE_TEMP,
        str(user_id)
    )

    os.makedirs(
        folder,
        exist_ok=True
    )

    return folder


def cleanup_user(
    user_id
):

    folder = os.path.join(
        BASE_TEMP,
        str(user_id)
    )

    try:

        if os.path.exists(
            folder
        ):

            shutil.rmtree(
                folder
            )

    except:
        pass


def save_photo(
    user_id,
    image_bytes,
    image_number
):

    folder = get_user_folder(
        user_id
    )

    image_path = os.path.join(
        folder,
        f"photo_{image_number}.jpg"
    )

    with open(
        image_path,
        "wb"
    ) as f:

        f.write(
            image_bytes
        )

    return image_path


def get_all_photos(
    user_id
):

    folder = get_user_folder(
        user_id
    )

    images = []

    for file in sorted(
        os.listdir(folder)
    ):

        if file.lower().endswith(
            (
                ".jpg",
                ".jpeg",
                ".png"
            )
        ):

            images.append(
                os.path.join(
                    folder,
                    file
                )
            )

    return images


def pdf_output_path(
    user_id,
    pdf_name
):

    folder = get_user_folder(
        user_id
    )

    return os.path.join(
        folder,
        f"{pdf_name}.pdf"
    )


def pdf_input_path(
    user_id
):

    folder = get_user_folder(
        user_id
    )

    return os.path.join(
        folder,
        "input.pdf"
    )


def image_output_path(
    user_id,
    page_no
):

    folder = get_user_folder(
        user_id
    )

    return os.path.join(
        folder,
        f"page_{page_no}.jpg"
    )
