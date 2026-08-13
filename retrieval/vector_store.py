from pathlib import Path

# pyrefly: ignore [missing-import]
from langchain_community.vectorstores import FAISS

from embeddings.embedding_model import (
    get_embedding_model
)


VECTOR_STORE_DIR = Path(
    "data/vector_store"
)


def create_vector_store(
    documents
):

    if not documents:

        raise ValueError(
            "No documents provided."
        )

    embeddings = get_embedding_model()

    vector_store = FAISS.from_documents(
        documents,
        embeddings
    )

    return vector_store


def save_vector_store(
    vector_store
):

    VECTOR_STORE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    vector_store.save_local(
        str(VECTOR_STORE_DIR)
    )


def load_vector_store():

    embeddings = get_embedding_model()

    if not VECTOR_STORE_DIR.exists():

        raise FileNotFoundError(
            "Vector store does not exist."
        )

    return FAISS.load_local(
        str(VECTOR_STORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )