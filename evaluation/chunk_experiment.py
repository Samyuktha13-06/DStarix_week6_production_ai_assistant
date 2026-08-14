import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from loaders.document_loader import load_documents
from loaders.chunk_documents import chunk_documents
from retrieval.vector_store import create_vector_store

import json


DOCUMENT_PATH = "documents/uploads/Internship Rule Book.pdf"
QUESTIONS_FILE = "evaluation/rag_questions.json"


CONFIGURATIONS = [
    {
        "name": "A",
        "chunk_size": 300,
        "chunk_overlap": 30
    },
    {
        "name": "B",
        "chunk_size": 500,
        "chunk_overlap": 50
    },
    {
        "name": "C",
        "chunk_size": 800,
        "chunk_overlap": 100
    }
]


def load_questions():

    with open(
        QUESTIONS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def evaluate_configuration(
    documents,
    questions,
    chunk_size,
    chunk_overlap
):

    chunks = chunk_documents(
        documents,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    vector_store = create_vector_store(
        chunks
    )

    total = 0
    hits = 0

    for item in questions:

        if not item["answerable"]:
            continue

        total += 1

        question = item["question"]

        expected_information = (
            item["expected_information"]
        )

        retrieved_documents = (
            vector_store.similarity_search(
                question,
                k=4
            )
        )

        retrieved_text = "\n".join(
            document.page_content
            for document in retrieved_documents
        ).lower()

        expected_words = [
            word.strip(".,!?():;\"'")
            for word in expected_information.lower().split()
            if len(
                word.strip(".,!?():;\"'")
            ) > 3
        ]

        matched_words = [
            word
            for word in expected_words
            if word in retrieved_text
        ]

        if expected_words:

            score = (
                len(matched_words)
                / len(expected_words)
            )

        else:

            score = 0

        if score >= 0.30:

            hits += 1

    hit_rate = (
        hits / total * 100
        if total
        else 0
    )

    return {
        "chunks": len(chunks),
        "hits": hits,
        "total": total,
        "hit_rate": hit_rate
    }


def main():

    print("\n" + "=" * 70)
    print("CHUNK SIZE / OVERLAP EXPERIMENT")
    print("=" * 70)

    documents = load_documents(
        DOCUMENT_PATH
    )

    questions = load_questions()

    results = []

    for config in CONFIGURATIONS:

        print(
            f"\nTesting configuration "
            f"{config['name']}"
        )

        print(
            f"Chunk size: "
            f"{config['chunk_size']}"
        )

        print(
            f"Chunk overlap: "
            f"{config['chunk_overlap']}"
        )

        result = evaluate_configuration(
            documents,
            questions,
            config["chunk_size"],
            config["chunk_overlap"]
        )

        result["configuration"] = config["name"]
        result["chunk_size"] = config["chunk_size"]
        result["chunk_overlap"] = config["chunk_overlap"]

        results.append(result)

        print(
            f"Number of chunks: "
            f"{result['chunks']}"
        )

        print(
            f"Retrieval hits: "
            f"{result['hits']}/{result['total']}"
        )

        print(
            f"Retrieval hit rate: "
            f"{result['hit_rate']:.2f}%"
        )

    print("\n" + "=" * 70)
    print("FINAL COMPARISON")
    print("=" * 70)

    print(
        f"{'Config':<10}"
        f"{'Size':<10}"
        f"{'Overlap':<10}"
        f"{'Chunks':<10}"
        f"{'Hit Rate':<12}"
    )

    print("-" * 70)

    for result in results:

        print(
            f"{result['configuration']:<10}"
            f"{result['chunk_size']:<10}"
            f"{result['chunk_overlap']:<10}"
            f"{result['chunks']:<10}"
            f"{result['hit_rate']:.2f}%"
        )


if __name__ == "__main__":

    main()