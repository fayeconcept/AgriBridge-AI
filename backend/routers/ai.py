from fastapi import APIRouter
from pydantic import BaseModel

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


class AIQuestion(BaseModel):
    question: str
    farm: FarmContext


@router.post("/ask")
def ask_ai(data: AIQuestion):

    answer = ask_agriculture_ai(
        data.question,
        data.farm
    )

    return {
        "answer": answer
    }