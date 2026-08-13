# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from pydantic import BaseModel
# pyrefly: ignore [missing-import]
from utils.chat import chat

app = FastAPI(
    title="DStarix AI Assistant",
    description=(
        "Production-ready AI Assistant integrating "
        "chat, RAG, memory, and tool calling."
    ),
    version="1.0.0"
)

class ChatRequest(BaseModel):

    session_id: str
    message: str

@app.get("/")
def root():

    return {
        "status": "running",
        "message": "DStarix AI Assistant API"
    }

@app.post("/chat")
def chat_endpoint(
    request: ChatRequest
):

    answer = chat(
        request.session_id,
        request.message
    )

    return {
        "session_id": request.session_id,
        "message": request.message,
        "answer": answer
    }    