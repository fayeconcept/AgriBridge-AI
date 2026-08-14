from typing import Optional
from pydantic import BaseModel, Field


# =========================================
# FARM CONTEXT
# =========================================

class FarmContext(BaseModel):
    farmer_name: str
    location: str
    state: str
    lga: str
    crop_type: str
    farm_size: float
    crop_age_weeks: Optional[float] = None


# =========================================
# CONVERSATION MESSAGE
# =========================================

class ConversationMessage(BaseModel):
    role: str
    content: str


# =========================================
# AI QUESTION
# =========================================

class AIQuestion(BaseModel):
    question: str
    farm: FarmContext

    conversation_history: list[ConversationMessage] = Field(
        default_factory=list
    )


# =========================================
# AI RESPONSE
# =========================================

class AIResponse(BaseModel):
    answer: str