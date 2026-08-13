from pathlib import Path

from loaders.document_loader import (
    validate_file
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