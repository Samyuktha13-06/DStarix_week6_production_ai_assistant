# pyrefly: ignore [missing-import]
from langgraph.graph import StateGraph, START, END

from graph.state import AssistantState
from graph.nodes.chat_node import chat_node


def build_assistant_graph():

    graph = StateGraph(
        AssistantState
    )

    graph.add_node(
        "chat",
        chat_node
    )

    graph.add_edge(
        START,
        "chat"
    )

    graph.add_edge(
        "chat",
        END
    )

    return graph.compile()