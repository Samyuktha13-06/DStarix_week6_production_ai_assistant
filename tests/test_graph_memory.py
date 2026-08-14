from graph.graph_builder import (
    build_assistant_graph
)


def test_conversation_memory_through_graph():

    graph = build_assistant_graph()

    session_id = "memory-test-session"

    first_result = graph.invoke(
        {
            "session_id": session_id,
            "question": "Hello"
        }
    )

    assert first_result["answer"]

    second_result = graph.invoke(
        {
            "session_id": session_id,
            "question": "Can you remember our conversation?"
        }
    )

    assert second_result["answer"]

    assert len(
        second_result["history"]
    ) >= 4