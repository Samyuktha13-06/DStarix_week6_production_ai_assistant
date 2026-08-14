# pyrefly: ignore [missing-import]
from tools.tools import calculator


TOOLS = [
    calculator
]


TOOL_REGISTRY = {
    tool.name: tool
    for tool in TOOLS
}


def get_tool(
    tool_name: str
):
    return TOOL_REGISTRY.get(
        tool_name
    )