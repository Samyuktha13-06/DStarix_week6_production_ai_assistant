import uuid
import requests
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


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="DStarix AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# Application Header
# --------------------------------------------------

st.title("🤖 DStarix AI Assistant")

st.caption(
    "Production-ready AI Assistant with Chat, RAG, "
    "Conversation Memory and Tool Calling"
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
# Display Previous Messages
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )

        # Display route if available
        if message.get("route"):

            st.caption(
                f"Route: {message['route']}"
            )

        # Display sources if available
        if (
            "sources" in message
            and message["sources"]
        ):

            with st.expander(
                "📚 View Sources"
            ):

                for idx, src in enumerate(
                    message["sources"],
                    start=1
                ):

                    page_info = (
                        f" (Page {src['page']})"
                        if src.get("page")
                        else ""
                    )

                    st.markdown(
                        f"**{idx}.** "
                        f"{src['source']}"
                        f"{page_info}"
                    )


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("📄 Document Upload")

    st.write(
        "Upload a PDF or text document "
        "to add it to the RAG knowledge base."
    )

    uploaded_file = st.file_uploader(
        "Upload a document",
        type=["pdf", "txt"],
        help=(
            "Supported formats: PDF and TXT"
        )
    )

    if uploaded_file:

        if st.button(
            "📥 Process Document",
            use_container_width=True
        ):

            try:

                # ----------------------------------
                # Save uploaded file
                # ----------------------------------

                file_path = save_uploaded_file(
                    uploaded_file
                )

                # ----------------------------------
                # Load document
                # ----------------------------------

                documents = load_documents(
                    file_path
                )

                # ----------------------------------
                # Chunk document
                # ----------------------------------

                chunks = chunk_documents(
                    documents
                )

                # ----------------------------------
                # Create vector store
                # ----------------------------------

                vector_store = create_vector_store(
                    chunks
                )

                # ----------------------------------
                # Save vector store
                # ----------------------------------

                save_vector_store(
                    vector_store
                )

                # ----------------------------------
                # Calculate extracted text
                # ----------------------------------

                document_text = "\n".join(
                    doc.page_content
                    for doc in documents
                )

                # ----------------------------------
                # Success message
                # ----------------------------------

                st.success(
                    "Document processed and added "
                    "to the vector store successfully."
                )

                st.info(
                    f"Extracted "
                    f"{len(document_text)} characters "
                    f"across "
                    f"{len(chunks)} chunks."
                )

            except Exception as e:

                st.error(
                    f"Document processing failed: {e}"
                )

    # --------------------------------------------------
    # Application Information
    # --------------------------------------------------

    st.markdown("---")

    st.header("⚙️ Assistant")

    st.info(
        "The assistant automatically routes "
        "each question to Chat, RAG, or Tool Calling."
    )

    st.markdown("---")

    st.header("🆔 Session")

    st.caption(
        "Current Session ID:"
    )

    st.code(
        st.session_state.session_id,
        language="text"
    )

    # --------------------------------------------------
    # Clear Conversation
    # --------------------------------------------------

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

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


# --------------------------------------------------
# Process User Question
# --------------------------------------------------

if question:

    # ----------------------------------------------
    # Add User Message
    # ----------------------------------------------

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message(
        "user"
    ):

        st.write(
            question
        )

    # ----------------------------------------------
    # Call Unified Assistant API
    # ----------------------------------------------

    try:

        response = requests.post(
            "http://127.0.0.1:8000/assistant",

            json={
                "session_id":
                    st.session_state.session_id,

                "message":
                    question
            },

            timeout=120
        )

        # Raise exception for HTTP errors
        response.raise_for_status()

        # ------------------------------------------
        # Parse API Response
        # ------------------------------------------

        data = response.json()

        answer = data.get(
            "answer",
            ""
        )

        route = data.get(
            "route",
            "unknown"
        )

        sources = data.get(
            "sources",
            []
        )

        # ------------------------------------------
        # Store Assistant Message
        # ------------------------------------------

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "route": route,
            "sources": sources
        })

        # ------------------------------------------
        # Display Assistant Response
        # ------------------------------------------

        with st.chat_message(
            "assistant"
        ):

            st.write(
                answer
            )

            # --------------------------------------
            # Display Route
            # --------------------------------------

            if route:

                st.caption(
                    f"Route: {route}"
                )

            # --------------------------------------
            # Display Sources
            # --------------------------------------

            if sources:

                with st.expander(
                    "📚 View Sources"
                ):

                    for idx, src in enumerate(
                        sources,
                        start=1
                    ):

                        page_info = (
                            f" (Page {src['page']})"
                            if src.get("page")
                            else ""
                        )

                        st.markdown(
                            f"**{idx}.** "
                            f"{src['source']}"
                            f"{page_info}"
                        )


    # ----------------------------------------------
    # FastAPI Connection Error
    # ----------------------------------------------

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Unable to connect to the FastAPI server."
        )

        st.info(
            "Start the API using:\n\n"
            "`uvicorn api.main:app --reload`"
        )


    # ----------------------------------------------
    # Request Timeout
    # ----------------------------------------------

    except requests.exceptions.Timeout:

        st.error(
            "⏱️ The request timed out. "
            "Please try again."
        )


    # ----------------------------------------------
    # HTTP Error
    # ----------------------------------------------

    except requests.exceptions.HTTPError as e:

        st.error(
            f"❌ API request failed: {e}"
        )

        try:

            error_detail = response.json()

            st.json(
                error_detail
            )

        except Exception:

            pass


    # ----------------------------------------------
    # Other Errors
    # ----------------------------------------------

    except Exception as e:

        st.error(
            f"❌ An unexpected error occurred: {e}"
        )