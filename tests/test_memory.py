from memory.conversation_memory import ConversationMemory


def test_conversation_memory():

    memory = ConversationMemory()

    session_id = "test-session"

    memory.add_user_message(
        session_id,
        "Hello"
    )

    memory.add_ai_message(
        session_id,
        "Hello! How can I help you?"
    )

    history = memory.get_history(
        session_id
    )

    assert len(history) == 2

    assert history[0].content == "Hello"

    assert (
        history[1].content
        == "Hello! How can I help you?"
    )


def test_clear_memory():

    memory = ConversationMemory()

    session_id = "test-session"

    memory.add_user_message(
        session_id,
        "Hello"
    )

    memory.clear(session_id)

    assert (
        memory.get_history(session_id)
        == []
    )