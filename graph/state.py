from typing import TypedDict, List

# pyrefly: ignore [missing-import]
from langchain_core.messages import BaseMessage


class AssistantState(TypedDict, total=False):

    session_id: str

    question: str

    history: List[BaseMessage]

    answer: str

    sources: List[dict]

    route: str

    tool_name: str

    tool_input: str

    tool_result: str