from loaders.document_loader import (
    load_documents
)

from loaders.chunk_documents import (
    chunk_documents
)


file_path = (
    "documents/uploads/"
    "Internship Rule Book.pdf"
)


documents = load_documents(
    file_path
)

print(
    f"Pages loaded: {len(documents)}"
)


chunks = chunk_documents(
    documents
)

print(
    f"Total chunks: {len(chunks)}"
)


for index, chunk in enumerate(
    chunks[:5],
    start=1
):

    print(
        f"\n--- Chunk {index} ---"
    )

    print(
        chunk.page_content[:500]
    )

    print(
        "Metadata:",
        chunk.metadata
    )