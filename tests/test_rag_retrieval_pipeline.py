from loaders.document_loader import (
    load_documents
)

from loaders.chunk_documents import (
    chunk_documents
)

from retrieval.retriever import (
    DocumentRetriever
)


DOCUMENT_PATH = (
    "documents/uploads/"
    "Internship Rule Book.pdf"
)


def test_full_retrieval_pipeline():

    documents = load_documents(
        DOCUMENT_PATH
    )

    assert len(documents) > 0

    chunks = chunk_documents(
        documents
    )

    assert len(chunks) > 0

    retriever = DocumentRetriever(
        chunks
    )

    results = retriever.search(
        "What is the internship duration?",
        k=3
    )

    assert len(results) > 0