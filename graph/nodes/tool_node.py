from graph.state import AssistantState

from tools.tool_registry import get_tool


def tool_node(
    state: AssistantState
) -> AssistantState:

    question = state["question"]

    tool_name = "calculator"

    expression = question

    prefixes = [
        "calculate",
        "calculator",
        "compute"
    ]

    for prefix in prefixes:

        expression = expression.replace(
            prefix,
            ""
        ).strip()

    tool = get_tool(
        tool_name
    )

    if tool is None:

        raise ValueError(
            f"Unknown tool: {tool_name}"
        )

    result = tool.invoke(
        expression
    )

    return {
        **state,
        "tool_name": tool_name,
        "tool_input": expression,
        "tool_result": result,
        "answer": f"The result is {result}."
    }