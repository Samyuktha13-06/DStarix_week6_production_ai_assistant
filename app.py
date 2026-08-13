import uuid

import requests
# pyrefly: ignore [missing-import]
import streamlit as st


st.set_page_config(
    page_title="DStarix AI Assistant",
    page_icon="🤖"
)


st.title("🤖 DStarix AI Assistant")

st.caption(
    "Conversational AI with persistent session memory"
)


# --------------------------------------------------
# Session ID
# --------------------------------------------------

if "session_id" not in st.session_state:

    st.session_state.session_id = str(
        uuid.uuid4()
    )


# --------------------------------------------------
# Chat History
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# --------------------------------------------------
# Display Messages
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )


with st.sidebar:

    st.subheader("Conversation")

    if st.button("🗑️ Clear Conversation"):

        st.session_state.messages = []

        st.session_state.session_id = str(
            uuid.uuid4()
        )

        st.rerun()

# --------------------------------------------------
# User Input
# --------------------------------------------------

question = st.chat_input(
    "Ask me anything..."
)


if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):

        st.write(question)

    try:

        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={
                "session_id":
                    st.session_state.session_id,
                "message": question
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        answer = data["answer"]

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        with st.chat_message(
            "assistant"
        ):

            st.write(answer)

    except requests.exceptions.ConnectionError:

        st.error(
            "Unable to connect to the FastAPI server."
        )

    except Exception as e:

        st.error(
            f"An error occurred: {e}"
        )


