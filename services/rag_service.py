from retrieval.vector_store import (
    load_vector_store
)

from utils.rag_answer import (
    generate_rag_answer
)

from utils.source_formatter import (
    format_sources
)


class RAGService:

    def __init__(self):

        self.vector_store = (
            load_vector_store()
        )

    def ask(
        self,
        question: str,
        k: int = 4
    ):

        documents = (
            self.vector_store.similarity_search(
                question,
                k=k
            )
        )

        answer = generate_rag_answer(
            question,
            documents
        )

        sources = format_sources(
            documents
        )

        return {
            "answer": answer,
            "sources": sources
        }