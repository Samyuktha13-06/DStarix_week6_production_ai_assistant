from pathlib import Path
import shutil

from loaders.document_loader import (
    validate_file
)


UPLOAD_DIR = Path(
    "documents/uploads"
)


UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


MAX_FILE_SIZE = 10 * 1024 * 1024


def save_uploaded_file(
    uploaded_file
) -> str:

    if not validate_file(
        uploaded_file.name
    ):

        raise ValueError(
            "Only PDF and TXT files are supported."
        )

    if uploaded_file.size > MAX_FILE_SIZE:

        raise ValueError(
            "File size must be less than 10 MB."
        )

    file_path = (
        UPLOAD_DIR /
        Path(
            uploaded_file.name
        ).name
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            uploaded_file,
            buffer
        )

    return str(file_path)