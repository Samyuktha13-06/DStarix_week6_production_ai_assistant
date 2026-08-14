import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.rag_service import RAGService


QUESTIONS_FILE = "evaluation/rag_questions.json"


def load_questions():

    with open(
        QUESTIONS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def normalize_text(text):

    return (
        text.lower()
        .replace(".", " ")
        .replace(",", " ")
        .replace("?", " ")
        .replace("!", " ")
        .replace(":", " ")
        .replace(";", " ")
    )


def calculate_keyword_coverage(
    answer,
    expected_information
):

    answer = normalize_text(answer)
    expected = normalize_text(
        expected_information
    )

    expected_words = [
        word
        for word in expected.split()
        if len(word) > 3
    ]

    if not expected_words:
        return 0.0

    matched = [
        word
        for word in expected_words
        if word in answer
    ]

    return (
        len(matched)
        / len(expected_words)
    )


def evaluate_answer(
    question,
    expected_information,
    answerable,
    result
):

    answer = result.get(
        "answer",
        ""
    )

    sources = result.get(
        "sources",
        []
    )

    # --------------------------------------------------
    # Answerable questions
    # --------------------------------------------------

    if answerable:

        coverage = calculate_keyword_coverage(
            answer,
            expected_information
        )

        correct = coverage >= 0.50

        grounded = len(sources) > 0

        return {
            "correct": correct,
            "grounded": grounded,
            "source_found": len(sources) > 0,
            "coverage": coverage
        }

    # --------------------------------------------------
    # Unanswerable questions
    # --------------------------------------------------

    answer_lower = answer.lower()

    refusal_phrases = [
        "not found",
        "not available",
        "cannot find",
        "can't find",
        "not mentioned",
        "not provided",
        "not contained",
        "no information",
        "unable to find",
        "do not have information",
        "does not contain"
    ]

    refused = any(
        phrase in answer_lower
        for phrase in refusal_phrases
    )

    # For an unanswerable question, a correct
    # grounded response should not invent an answer.

    return {
        "correct": refused,
        "grounded": refused,
        "source_found": len(sources) > 0,
        "coverage": 1.0 if refused else 0.0
    }


def main():

    questions = load_questions()

    rag_service = RAGService()

    answerable_total = 0
    correct_answers = 0

    grounded_total = 0
    grounded_answers = 0

    print("\n" + "=" * 70)
    print("RAG ANSWER QUALITY EVALUATION")
    print("=" * 70)

    for item in questions:

        question = item["question"]

        expected_information = (
            item["expected_information"]
        )

        answerable = item["answerable"]

        print("\n" + "-" * 70)

        print(
            f"Q{item['id']}: {question}"
        )

        try:

            result = rag_service.ask(
                question
            )

            answer = result.get(
                "answer",
                ""
            )

            evaluation = evaluate_answer(
                question,
                expected_information,
                answerable,
                result
            )

            print("\nGenerated answer:")
            print(answer)

            print(
                f"\nKeyword coverage: "
                f"{evaluation['coverage']:.2f}"
            )

            print(
                "Correctness: "
                f"{'PASS' if evaluation['correct'] else 'FAIL'}"
            )

            print(
                "Grounded: "
                f"{'PASS' if evaluation['grounded'] else 'FAIL'}"
            )

            print(
                "Sources available: "
                f"{'YES' if evaluation['source_found'] else 'NO'}"
            )

            if answerable:

                answerable_total += 1

                if evaluation["correct"]:
                    correct_answers += 1

                grounded_total += 1

                if evaluation["grounded"]:
                    grounded_answers += 1

        except Exception as e:

            print(
                f"\nERROR: {e}"
            )

    print("\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)

    if answerable_total:

        accuracy = (
            correct_answers
            / answerable_total
            * 100
        )

        grounded_rate = (
            grounded_answers
            / grounded_total
            * 100
        )

        print(
            f"Answer accuracy: "
            f"{accuracy:.2f}%"
        )

        print(
            f"Grounded response rate: "
            f"{grounded_rate:.2f}%"
        )

        print(
            f"Correct answers: "
            f"{correct_answers}/{answerable_total}"
        )

        print(
            f"Grounded answers: "
            f"{grounded_answers}/{grounded_total}"
        )

    print("=" * 70)


if __name__ == "__main__":

    main()