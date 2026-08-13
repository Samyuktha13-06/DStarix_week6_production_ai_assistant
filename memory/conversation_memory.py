from typing import Dict, List

# pyrefly: ignore [missing-import]
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    BaseMessage
)


class ConversationMemory:

    def __init__(self):

        self.conversations: Dict[
            str,
            List[BaseMessage]
        ] = {}

    def get_history(
        self,
        session_id: str
    ) -> List[BaseMessage]:

        return self.conversations.get(
            session_id,
            []
        )

    def add_user_message(
        self,
        session_id: str,
        message: str
    ):

        if session_id not in self.conversations:

            self.conversations[
                session_id
            ] = []

        self.conversations[
            session_id
        ].append(
            HumanMessage(
                content=message
            )
        )

    def add_ai_message(
        self,
        session_id: str,
        message: str
    ):

        if session_id not in self.conversations:

            self.conversations[
                session_id
            ] = []

        self.conversations[
            session_id
        ].append(
            AIMessage(
                content=message
            )
        )

    def clear(
        self,
        session_id: str
    ):

        self.conversations.pop(
            session_id,
            None
        )