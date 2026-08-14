from graph.state import AssistantState

from tools.tool_registry import (
    get_tool
)


def tool_node(
    state: AssistantState
) -> AssistantState:

    tool_name = state.get(
        "tool_name"
    )

    tool_input = state.get(
        "tool_input"
    )

    if not tool_name:

        return {
            **state,
            "tool_result": None
        }

    tool = get_tool(
        tool_name
    )

    if tool is None:

        raise ValueError(
            f"Unknown tool: {tool_name}"
        )

    result = tool.invoke(
        tool_input
    )

    return {
        **state,
        "tool_result": result
    }