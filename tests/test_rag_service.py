# pyrefly: ignore [missing-import]
from langchain_core.documents import Document

from utils.source_formatter import (
    format_sources
)


def test_source_formatter():

    documents = [

        Document(
            page_content="Test content",
            metadata={
                "source": "company.pdf",
                "page": 2
            }
        ),

        Document(
            page_content="More content",
            metadata={
                "source": "company.pdf",
                "page": 5
            }
        )

    ]

    sources = format_sources(
        documents
    )

    assert len(sources) == 2

    assert sources[0]["source"] == "company.pdf"
    assert sources[0]["page"] == 2