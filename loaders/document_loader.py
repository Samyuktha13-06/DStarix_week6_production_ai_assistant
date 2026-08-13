from pathlib import Path

# pyrefly: ignore [missing-import]
from langchain_core.documents import Document
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


def load_pdf_documents(
    file_path: str
):

    reader = PdfReader(
        file_path
    )

    documents = []

    filename = Path(
        file_path
    ).name

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = page.extract_text()

        if text and text.strip():

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": filename,
                        "page": page_number
                    }
                )
            )

    return documents

def load_txt_documents(
    file_path: str
):

    filename = Path(
        file_path
    ).name

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    if not text.strip():

        return []

    return [
        Document(
            page_content=text,
            metadata={
                "source": filename,
                "page": None
            }
        )
    ]

def load_documents(
    file_path: str
):

    extension = Path(
        file_path
    ).suffix.lower()

    if extension == ".pdf":

        return load_pdf_documents(
            file_path
        )

    if extension == ".txt":

        return load_txt_documents(
            file_path
        )

    raise ValueError(
        f"Unsupported file type: {extension}"
    )


def load_document(
    file_path: str
) -> str:

    documents = load_documents(
        file_path
    )

    return "\n".join(
        doc.page_content
        for doc in documents
    )