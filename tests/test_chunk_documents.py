# pyrefly: ignore [missing-import]
from langchain_core.documents import Document

from loaders.chunk_documents import (
    chunk_documents
)


def test_metadata_is_preserved():

    documents = [
        Document(
            page_content=(
                "This is a sample document. "
                * 100
            ),
            metadata={
                "source": "sample.pdf",
                "page": 2
            }
        )
    ]

    chunks = chunk_documents(
        documents
    )

    assert len(chunks) > 1

    for chunk in chunks:

        assert chunk.metadata[
            "source"
        ] == "sample.pdf"

        assert chunk.metadata[
            "page"
        ] == 2