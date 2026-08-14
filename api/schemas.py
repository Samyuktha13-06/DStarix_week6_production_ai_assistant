from typing import List, Dict, Any

# pyrefly: ignore [missing-import]
from pydantic import BaseModel


class AssistantRequest(BaseModel):

    session_id: str
    message: str


class AssistantResponse(BaseModel):

    session_id: str
    message: str
    answer: str
    route: str
    sources: List[Dict[str, Any]] = []