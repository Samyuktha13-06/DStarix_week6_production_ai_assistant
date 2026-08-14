import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from retrieval.vector_store import load_vector_store


QUESTIONS_FILE = "evaluation/rag_questions.json"


def load_questions():

    with open(
        QUESTIONS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def evaluate_retrieval(k=4):

    questions = load_questions()

    vector_store = load_vector_store()

    total = 0
    hits = 0

    print("\n" + "=" * 60)
    print(f"RAG RETRIEVAL EVALUATION | k={k}")
    print("=" * 60)

    for item in questions:

        question = item["question"]

        expected_information = (
            item["expected_information"]
        )

        answerable = item["answerable"]

        documents = (
            vector_store.similarity_search(
                question,
                k=k
            )
        )

        retrieved_text = "\n".join(
            document.page_content
            for document in documents
        ).lower()

        # --------------------------------------------------
        # Unanswerable question
        # --------------------------------------------------

        if not answerable:

            print(f"\nQ{item['id']}: {question}")

            if documents:

                print(
                    "   Retrieved documents: "
                    f"{len(documents)}"
                )

            print(
                "   [OK] Unanswerable question "
                "included in evaluation"
            )

            continue

        # --------------------------------------------------
        # Answerable question
        # --------------------------------------------------

        total += 1

        # Use important words from the expected
        # information rather than requiring an
        # exact string match.

        expected_words = [
            word.strip(".,!?():;\"'")
            for word in expected_information.lower().split()
            if len(word.strip(".,!?():;\"'")) > 3
        ]

        matched_words = [
            word
            for word in expected_words
            if word in retrieved_text
        ]

        # At least 30% of meaningful expected words
        # should occur in retrieved context.

        if expected_words:

            score = (
                len(matched_words)
                / len(expected_words)
            )

        else:

            score = 0

        hit = score >= 0.30

        if hit:
            hits += 1

        print(f"\nQ{item['id']}: {question}")

        print(
            f"   Retrieved chunks: {len(documents)}"
        )

        print(
            f"   Match score: {score:.2f}"
        )

        print(
            f"   Result: {'HIT' if hit else 'MISS'}"
        )

        # Show sources

        for document in documents:

            source = document.metadata.get(
                "source",
                "Unknown"
            )

            page = document.metadata.get(
                "page"
            )

            print(
                f"   Source: {source}"
                f"{f' | Page {page}' if page else ''}"
            )

    print("\n" + "=" * 60)

    if total > 0:

        hit_rate = (
            hits / total
        ) * 100

        print(
            f"Retrieval Hit Rate: "
            f"{hit_rate:.2f}%"
        )

        print(
            f"Hits: {hits}/{total}"
        )

    print("=" * 60)


if __name__ == "__main__":

    for k in [2, 4, 6]:

        evaluate_retrieval(k=k)