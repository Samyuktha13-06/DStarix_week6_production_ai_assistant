from graph.state import AssistantState

from memory.conversation_memory import ConversationMemory

from utils.llm import llm


memory = ConversationMemory()


def chat_node(
    state: AssistantState
) -> AssistantState:

    session_id = state["session_id"]

    question = state["question"]

    history = memory.get_history(
        session_id
    )

    messages = list(history)

    messages.append(
        (
            "human",
            question
        )
    )

    response = llm.invoke(
        messages
    )

    answer = response.content

    memory.add_user_message(
        session_id,
        question
    )

    memory.add_ai_message(
        session_id,
        answer
    )

    return {
        **state,
        "history": memory.get_history(
            session_id
        ),
        "answer": answer
    }