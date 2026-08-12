from fastapi import APIRouter
from backend.schemas.ai import AIQuestion, AIResponse
from ai_engine.gemini import ask_agriculture_ai

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.post("/ask", response_model=AIResponse)
def ask_ai(data: AIQuestion):
    answer = ask_agriculture_ai(
        data.question,
        data.farm,
        data.conversation_history
    )

    return {
        "answer": answer
    }


@router.get("/health")
def ai_health():
    return {
        "status": "AI service is running",
        "service": "AgriBridge AI"
    }


@router.get("/info")
def ai_info():
    return {
        "service": "AgriBridge AI",
        "provider": "Google Gemini",
        "status": "AI integration configured"
    }