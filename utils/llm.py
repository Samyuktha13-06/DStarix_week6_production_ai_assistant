# pyrefly: ignore [missing-import]
from groq import Groq
from langchain_groq import ChatGroq

from utils.config import GROQ_API_KEY


client = Groq(
    api_key=GROQ_API_KEY
)


MODEL_NAME = "llama-3.3-70b-versatile"


llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=MODEL_NAME,
    temperature=0.2
)


def generate_response(
    prompt: str
) -> str:

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content