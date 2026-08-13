# pyrefly: ignore [missing-import]
from retrieval.vector_store import (
    create_vector_store
)


class DocumentRetriever:

    def __init__(
        self,
        documents
    ):

        self.vector_store = (
            create_vector_store(
                documents
            )
        )

    def search(
        self,
        query: str,
        k: int = 4
    ):

        return self.vector_store.similarity_search(
            query,
            k=k
        )