from pathlib import Path

# pyrefly: ignore [missing-import]
from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".txt"
}


def validate_file(
    filename: str
) -> bool:

    extension = Path(
        filename
    ).suffix.lower()

    return extension in SUPPORTED_EXTENSIONS


def load_pdf(
    file_path: str
) -> str:

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n\n".join(pages)


def load_text(
    file_path: str
) -> str:

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def load_document(
    file_path: str
) -> str:

    extension = Path(
        file_path
    ).suffix.lower()

    if extension == ".pdf":

        return load_pdf(
            file_path
        )

    if extension == ".txt":

        return load_text(
            file_path
        )

    raise ValueError(
        f"Unsupported file type: {extension}"
    )