# pyrefly: ignore [missing-import]
from fastapi import FastAPI


app = FastAPI(
    title="DStarix AI Assistant",
    description=(
        "Production-ready AI Assistant integrating "
        "chat, RAG, memory, and tool calling."
    ),
    version="1.0.0"
)


@app.get("/")
def root():

    return {
        "status": "running",
        "message": "DStarix AI Assistant API"
    }