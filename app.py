# pyrefly: ignore [missing-import]
import streamlit as st


st.set_page_config(
    page_title="DStarix AI Assistant",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 DStarix AI Assistant")

st.markdown(
    """
    Welcome to the DStarix AI Assistant.

    This application will integrate:

    - 💬 Conversational AI
    - 📚 Document-based RAG
    - 🧠 Conversation memory
    - 🛠️ Tool calling
    - 📄 Document upload
    - 🔎 Source-aware answers
    """
)


st.info(
    "Phase 1: Base application setup completed."
)