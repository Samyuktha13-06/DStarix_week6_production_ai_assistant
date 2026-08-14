from graph.nodes.tool_node import (
    tool_node
)


def test_tool_node():

    state = {
        "tool_name": "calculator",
        "tool_input": "125 * 48"
    }

    result = tool_node(
        state
    )

    assert result["tool_result"] == "6000"