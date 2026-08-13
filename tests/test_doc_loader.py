from pathlib import Path

from loaders.document_loader import (
    validate_file,
    load_document
)


def test_pdf_is_supported():

    assert validate_file(
        "document.pdf"
    )


def test_txt_is_supported():

    assert validate_file(
        "document.txt"
    )


def test_image_is_not_supported():

    assert not validate_file(
        "image.jpg"
    )


def test_load_txt_document(tmp_path):

    p = tmp_path / "test_doc.txt"
    p.write_text("Hello, DStarix!", encoding="utf-8")

    content = load_document(str(p))

    assert content == "Hello, DStarix!"