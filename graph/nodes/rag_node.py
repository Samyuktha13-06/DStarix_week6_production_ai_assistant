from graph.state import AssistantState

from services.rag_service import RAGService


def rag_node(
    state: AssistantState
) -> AssistantState:

    question = state["question"]

    service = RAGService()

    result = service.ask(
        question
    )

    return {
        **state,
        "answer": result["answer"],
        "sources": result.get(
            "sources",
            []
        )
    }