from utils.llm import llm


RAG_PROMPT = """
You are a document-based AI assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer cannot be found in the context,
say:

"I could not find this information in the uploaded documents."

Do not invent information.
Do not use outside knowledge.

Context:
{context}

Question:
{question}

Answer:
"""


def generate_rag_answer(
    question: str,
    documents
) -> str:

    if not documents:

        return (
            "I could not find this information "
            "in the uploaded documents."
        )

    context_parts = []

    for document in documents:

        context_parts.append(
            document.page_content
        )

    context = "\n\n---\n\n".join(
        context_parts
    )

    prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )

    response = llm.invoke(
        prompt
    )

    return response.content