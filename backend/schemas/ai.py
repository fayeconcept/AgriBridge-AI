from pydantic import BaseModel
from typing import Optional


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


class AIResponse(BaseModel):
    answer: str