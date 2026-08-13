import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from loaders.document_loader import (
    load_documents
)

from loaders.chunk_documents import (
    chunk_documents
)

from retrieval.vector_store import (
    create_vector_store,
    save_vector_store
)


DOCUMENT_PATH = (
    "documents/uploads/"
    "Internship Rule Book.pdf"
)


def main():

    print(
        "Loading document..."
    )

    documents = load_documents(
        DOCUMENT_PATH
    )

    print(
        f"Loaded {len(documents)} pages."
    )

    print(
        "Creating chunks..."
    )

    chunks = chunk_documents(
        documents
    )

    print(
        f"Created {len(chunks)} chunks."
    )

    print(
        "Creating embeddings..."
    )

    vector_store = create_vector_store(
        chunks
    )

    print(
        "Saving vector store..."
    )

    save_vector_store(
        vector_store
    )

    print(
        "Vector store created successfully."
    )


if __name__ == "__main__":

    main()