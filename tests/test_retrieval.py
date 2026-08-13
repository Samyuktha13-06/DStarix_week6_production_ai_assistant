# pyrefly: ignore [missing-import]
from langchain_core.documents import Document

from retrieval.retriever import (
    DocumentRetriever
)


def test_retrieval():

    documents = [

        Document(
            page_content=(
                "The internship duration "
                "is six weeks."
            ),
            metadata={
                "source": "test.pdf",
                "page": 1
            }
        ),

        Document(
            page_content=(
                "Interns must submit "
                "their weekly assignments."
            ),
            metadata={
                "source": "test.pdf",
                "page": 2
            }
        ),

        Document(
            page_content=(
                "The internship focuses "
                "on artificial intelligence."
            ),
            metadata={
                "source": "test.pdf",
                "page": 3
            }
        )

    ]

    retriever = DocumentRetriever(
        documents
    )

    results = retriever.search(
        "How long is the internship?",
        k=2
    )

    assert len(results) > 0

    assert any(
        "duration" in doc.page_content.lower()
        for doc in results
    )