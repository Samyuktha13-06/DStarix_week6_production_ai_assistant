from graph.graph_builder import (
    build_assistant_graph
)


def test_graph_builds():

    graph = build_assistant_graph()

    assert graph is not None


def test_graph_state():

    graph = build_assistant_graph()

    result = graph.invoke(
        {
            "session_id": "test-session",
            "question": "Hello"
        }
    )

    assert "answer" in result

    assert result["answer"]