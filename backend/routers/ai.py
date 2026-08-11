from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from ai_engine.gemini import ask_agriculture_ai


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


class FarmContext(BaseModel):
    farmer_name: str
    location: str
    state: str
    lga: str
    crop_type: str
    farm_size: float
    crop_age_weeks: Optional[float] = None


class AIQuestion(BaseModel):
    question: str
    farm: FarmContext
    conversation_history: list[str] = []


@router.post("/ask")
def ask_ai(data: AIQuestion):

    answer = ask_agriculture_ai(
        data.question,
        data.farm,
        data.conversation_history
    )

    return {
        "answer": answer
    }