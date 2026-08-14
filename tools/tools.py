# pyrefly: ignore [missing-import]
from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """
    Evaluate a basic mathematical expression.

    Use this tool when the user asks for a
    mathematical calculation.
    """

    allowed_characters = (
        "0123456789+-*/().% "
    )

    if not expression.strip():
        raise ValueError(
            "Expression cannot be empty."
        )

    if any(
        character not in allowed_characters
        for character in expression
    ):
        raise ValueError(
            "Invalid characters in expression."
        )

    try:

        result = eval(
            expression,
            {
                "__builtins__": {}
            },
            {}
        )

        return str(result)

    except Exception as exc:

        raise ValueError(
            f"Invalid mathematical expression: {expression}"
        ) from exc