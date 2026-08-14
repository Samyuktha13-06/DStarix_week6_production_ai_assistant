# pyrefly: ignore [missing-import]
from langgraph.graph import (
    StateGraph,
    START,
    END
)

from graph.state import AssistantState

from graph.nodes.router_node import (
    router_node
)

from graph.nodes.chat_node import (
    chat_node
)

from graph.nodes.rag_node import (
    rag_node
)

from graph.nodes.tool_node import (
    tool_node
)


def route_question(
    state: AssistantState
):

    return state["route"]


def build_assistant_graph():

    graph = StateGraph(
        AssistantState
    )

    graph.add_node(
        "router",
        router_node
    )

    graph.add_node(
        "chat",
        chat_node
    )

    graph.add_node(
        "rag",
        rag_node
    )

    graph.add_node(
        "tool",
        tool_node
    )

    graph.add_edge(
        START,
        "router"
    )

    graph.add_conditional_edges(
        "router",
        route_question,
        {
            "chat": "chat",
            "rag": "rag",
            "tool": "tool"
        }
    )

    graph.add_edge(
        "chat",
        END
    )

    graph.add_edge(
        "rag",
        END
    )

    graph.add_edge(
        "tool",
        END
    )

    return graph.compile()