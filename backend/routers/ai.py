from fastapi import APIRouter
from pydantic import BaseModel

from ai_engine.gemini import ask_agriculture_ai


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


class AIQuestion(BaseModel):
    question: str


@router.post("/ask")
def ask_ai(data: AIQuestion):
    answer = ask_agriculture_ai(data.question)

    return {
        "answer": answer
    }