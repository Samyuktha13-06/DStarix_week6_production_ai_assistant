# pyrefly: ignore [missing-import]

from fastapi import FastAPI

from api.schemas import (
    AssistantRequest,
    AssistantResponse
)

from graph.graph_builder import (
    build_assistant_graph
)


app = FastAPI(
    title="DStarix AI Assistant",
    description=(
        "Production-ready AI Assistant integrating "
        "chat, RAG, memory, and tool calling."
    ),
    version="1.0.0"
)


assistant_graph = build_assistant_graph()


@app.get("/")
def root():

    return {
        "status": "running",
        "message": "DStarix AI Assistant API"
    }


@app.post(
    "/assistant",
    response_model=AssistantResponse
)
def assistant_endpoint(
    request: AssistantRequest
):

    result = assistant_graph.invoke(
        {
            "session_id": request.session_id,
            "question": request.message
        }
    )

    return {
        "session_id": request.session_id,
        "message": request.message,
        "answer": result.get(
            "answer",
            ""
        ),
        "route": result.get(
            "route",
            "unknown"
        ),
        "sources": result.get(
            "sources",
            []
        )
    }