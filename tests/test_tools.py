from tools.tools import calculator


def test_calculator():

    result = calculator.invoke(
        "125 * 48"
    )

    assert result == "6000"


def test_calculator_addition():

    result = calculator.invoke(
        "100 + 50"
    )

    assert result == "150"


def test_calculator_invalid_expression():

    try:

        calculator.invoke(
            "import os"
        )

        assert False

    except ValueError:

        assert True


from tools.tool_registry import (
    get_tool
)


def test_tool_registry():

    tool = get_tool(
        "calculator"
    )

    assert tool is not None

    assert tool.name == "calculator"