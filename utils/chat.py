from utils.llm import client, MODEL_NAME
from memory.conversation_memory import ConversationMemory


memory = ConversationMemory()


def chat(
    session_id: str,
    question: str
) -> str:

    history = memory.get_history(
        session_id
    )

    messages = []

    for message in history:

        if message.type == "human":

            messages.append({
                "role": "user",
                "content": message.content
            })

        elif message.type == "ai":

            messages.append({
                "role": "assistant",
                "content": message.content
            })

    messages.append({
        "role": "user",
        "content": question
    })

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.2
    )

    answer = response.choices[
        0
    ].message.content

    memory.add_user_message(
        session_id,
        question
    )

    memory.add_ai_message(
        session_id,
        answer
    )

    return answer