from typing import TypedDict, List

# pyrefly: ignore [missing-import]
from langchain_core.messages import BaseMessage


class AssistantState(TypedDict, total=False):

    session_id: str

    question: str

    history: List[BaseMessage]

    answer: str