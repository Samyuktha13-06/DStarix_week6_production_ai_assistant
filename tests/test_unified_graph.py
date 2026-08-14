from graph.graph_builder import (
    build_assistant_graph
)


def test_chat_route():

    graph = build_assistant_graph()

    result = graph.invoke(
        {
            "session_id": "chat-test",
            "question": "Hello, how are you?"
        }
    )

    assert result["route"] == "chat"
    assert result["answer"]


def test_rag_route():

    graph = build_assistant_graph()

    result = graph.invoke(
        {
            "session_id": "rag-test",
            "question": (
                "What are the internship "
                "working days?"
            )
        }
    )

    assert result["route"] == "rag"
    assert result["answer"]


def test_tool_route():

    graph = build_assistant_graph()

    result = graph.invoke(
        {
            "session_id": "tool-test",
            "question": "calculate 125 * 48"
        }
    )

    assert result["route"] == "tool"
    assert result["tool_result"] == "6000"
    assert result["answer"]