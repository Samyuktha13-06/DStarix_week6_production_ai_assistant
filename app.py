import uuid
from services.rag_service import (
    RAGService
)
import requests
# pyrefly: ignore [missing-import]
import streamlit as st
from utils.file_manager import (
    save_uploaded_file
)

from loaders.document_loader import (
    load_documents
)
from loaders.chunk_documents import (
    chunk_documents
)
from retrieval.vector_store import (
    create_vector_store,
    save_vector_store
)

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

        if "sources" in message and message["sources"]:

            with st.expander("📚 View Sources"):

                for idx, src in enumerate(message["sources"], start=1):

                    page_info = f" (Page {src['page']})" if src.get("page") else ""
                    st.markdown(f"**{idx}.** {src['source']}{page_info}")


with st.sidebar:

    st.header("📄 Document Upload")

    uploaded_file = st.file_uploader(
        "Upload a document",
        type=["pdf", "txt"],
        help="Upload a PDF or text document."
    )

    if uploaded_file:

        if st.button(
            "📥 Process Document"
        ):

            try:

                file_path = (
                    save_uploaded_file(
                        uploaded_file
                    )
                )

                documents = load_documents(
                    file_path
                )

                chunks = chunk_documents(
                    documents
                )

                vector_store = create_vector_store(
                    chunks
                )

                save_vector_store(
                    vector_store
                )

                document_text = "\n".join(
                    doc.page_content
                    for doc in documents
                )

                st.success(
                    "Document processed and added to vector store successfully."
                )

                st.info(
                    f"Extracted {len(document_text)} characters across {len(chunks)} chunks."
                )

            except Exception as e:

                st.error(
                    f"Document processing failed: {e}"
                )

    st.markdown("---")
    st.header("⚙️ Settings")
    use_rag = st.checkbox(
        "Enable RAG (Query documents)",
        value=False,
        help="If enabled, answers will be retrieved from the uploaded documents."
    )

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

        if use_rag:

            try:

                rag_service = RAGService()

                result = rag_service.ask(
                    question
                )

                answer = result["answer"]
                sources = result.get("sources", [])

            except FileNotFoundError:

                answer = (
                    "No document has been processed yet. "
                    "Please upload and process a document in the sidebar first."
                )
                sources = []

            except Exception as e:

                answer = f"Error querying RAG service: {e}"
                sources = []

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })

            with st.chat_message(
                "assistant"
            ):

                st.write(answer)

                if sources:

                    with st.expander("📚 View Sources"):

                        for idx, src in enumerate(sources, start=1):

                            page_info = f" (Page {src['page']})" if src.get("page") else ""
                            st.markdown(f"**{idx}.** {src['source']}{page_info}")

        else:

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


