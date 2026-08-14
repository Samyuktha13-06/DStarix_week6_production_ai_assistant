# pyrefly: ignore [missing-import]
from retrieval.vector_store import (
    load_vector_store
)

from utils.rag_answer import (
    generate_rag_answer
)

from utils.source_formatter import (
    format_sources
)


def test_end_to_end_rag():

    vector_store = load_vector_store()

    documents = (
        vector_store.similarity_search(
            "What is the internship duration?",
            k=4
        )
    )

    assert len(documents) > 0

    sources = format_sources(
        documents
    )

    assert len(sources) > 0

    answer = generate_rag_answer(
        "What is the internship duration?",
        documents
    )

    assert answer
    assert isinstance(
        answer,
        str
    )