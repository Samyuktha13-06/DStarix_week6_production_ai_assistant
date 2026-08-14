from graph.state import AssistantState


def router_node(
    state: AssistantState
) -> AssistantState:

    question = state["question"].lower()

    tool_keywords = [
        "calculate",
        "calculator",
        "compute",
        "multiply",
        "divide",
        "add",
        "subtract"
    ]

    rag_keywords = [
        "document",
        "internship",
        "rule",
        "policy",
        "working",
        "intern",
        "dstarix"
    ]

    if any(
        keyword in question
        for keyword in tool_keywords
    ):
        route = "tool"

    elif any(
        keyword in question
        for keyword in rag_keywords
    ):
        route = "rag"

    else:
        route = "chat"

    return {
        **state,
        "route": route
    }