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
    farm_context = f"""
Farmer Name: {data.farm.farmer_name}
Location: {data.farm.location}
State: {data.farm.state}
LGA: {data.farm.lga}
Crop Type: {data.farm.crop_type}
Farm Size: {data.farm.farm_size} hectares
"""

    full_question = f"""
Farmer Information:
{farm_context}

Farmer's Question:
{data.question}
"""

    answer = ask_agriculture_ai(full_question)

    return {
        "answer": answer
    }