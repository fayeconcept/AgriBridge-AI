from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.schemas.ai import AIQuestion, AIResponse
from ai_engine.gemini import ask_agriculture_ai

from backend.core.database import SessionLocal
from backend.models.ai_conversation import AIConversation
from backend.core.conversation import get_conversation_history


# =========================================================
# AI ROUTER
# =========================================================

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


# =========================================================
# DATABASE SESSION
# =========================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =========================================================
# ASK AGRIBRIDGE AI
# =========================================================

@router.post(
    "/ask",
    response_model=AIResponse
)
def ask_ai(
    data: AIQuestion,
    db: Session = Depends(get_db)
):

    try:

        # =================================================
        # GET PREVIOUS CONVERSATION FROM DATABASE
        # =================================================

        previous_messages = get_conversation_history(
            db=db,
            farmer_name=data.farm.farmer_name,
            limit=10
        )


        # =================================================
        # CONVERT DATABASE HISTORY TO AI FORMAT
        # =================================================

        conversation_history = []

        for message in previous_messages:

            conversation_history.append({
                "role": message.role,
                "content": message.content
            })


        # =================================================
        # SEND REQUEST TO GEMINI
        # =================================================

        answer = ask_agriculture_ai(
            question=data.question,
            farm_context=data.farm,
            conversation_history=conversation_history
        )


        # =================================================
        # CHECK FOR GEMINI ERROR MESSAGES
        # =================================================

        if (
            "temporarily unable to process" in answer.lower()
            or "usage limit" in answer.lower()
            or "high demand" in answer.lower()
            or "temporary gemini" in answer.lower()
        ):

            return AIResponse(
                answer=answer
            )


        # =================================================
        # SAVE FARMER QUESTION
        # =================================================

        farmer_message = AIConversation(
            farmer_name=data.farm.farmer_name,
            role="user",
            content=data.question
        )

        db.add(farmer_message)


        # =================================================
        # SAVE REAL AI RESPONSE
        # =================================================

        ai_message = AIConversation(
            farmer_name=data.farm.farmer_name,
            role="assistant",
            content=answer
        )

        db.add(ai_message)

        db.commit()


        # =================================================
        # RETURN AI RESPONSE
        # =================================================

        return AIResponse(
            answer=answer
        )


    # =====================================================
    # HANDLE ERRORS
    # =====================================================

    except Exception as e:

        db.rollback()

        print(
            "AI ROUTER ERROR:",
            repr(e)
        )

        error_text = str(e)


        # =================================================
        # 429 - QUOTA / RATE LIMIT
        # =================================================

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
            or "rate limit" in error_text.lower()
        ):

            raise HTTPException(
                status_code=429,
                detail={
                    "error": "quota_exceeded",
                    "message": (
                        "AgriBridge AI is temporarily unable "
                        "to process your request because the "
                        "Gemini AI service has reached its "
                        "current usage limit. Please try again "
                        "later."
                    )
                }
            )


        # =================================================
        # 503 - GEMINI UNAVAILABLE
        # =================================================

        if (
            "503" in error_text
            or "UNAVAILABLE" in error_text
        ):

            raise HTTPException(
                status_code=503,
                detail={
                    "error": "ai_unavailable",
                    "message": (
                        "AgriBridge AI is temporarily "
                        "unavailable because the Gemini "
                        "AI service is experiencing high "
                        "demand. Please try again shortly."
                    )
                }
            )


        # =================================================
        # 400 - INVALID REQUEST
        # =================================================

        if (
            "400" in error_text
            or "INVALID_ARGUMENT" in error_text
        ):

            raise HTTPException(
                status_code=400,
                detail={
                    "error": "invalid_request",
                    "message": (
                        "AgriBridge AI could not process "
                        "this request. Please check the "
                        "information provided."
                    )
                }
            )


        # =================================================
        # 401 / 403 - API KEY OR PERMISSION
        # =================================================

        if (
            "401" in error_text
            or "403" in error_text
            or "UNAUTHENTICATED" in error_text
            or "PERMISSION_DENIED" in error_text
        ):

            raise HTTPException(
                status_code=503,
                detail={
                    "error": "ai_authentication_error",
                    "message": (
                        "AgriBridge AI could not connect "
                        "to the Gemini AI service. Please "
                        "check the Gemini API configuration."
                    )
                }
            )


        # =================================================
        # UNEXPECTED ERROR
        # =================================================

        raise HTTPException(
            status_code=500,
            detail={
                "error": "ai_error",
                "message": (
                    "AgriBridge AI encountered an unexpected "
                    "problem. Please try again."
                )
            }
        )


# =========================================================
# CONVERSATION HISTORY
# =========================================================

@router.get(
    "/conversation/{farmer_name}"
)
def get_farmer_conversation(
    farmer_name: str,
    db: Session = Depends(get_db)
):

    messages = get_conversation_history(
        db=db,
        farmer_name=farmer_name,
        limit=10
    )

    return {
        "farmer_name": farmer_name,
        "count": len(messages),
        "conversation": [
            {
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at
            }
            for message in messages
        ]
    }


# =========================================================
# AI HEALTH CHECK
# =========================================================

@router.get("/health")
def ai_health():

    return {
        "status": "AI service is running",
        "service": "AgriBridge AI"
    }


# =========================================================
# AI INFORMATION
# =========================================================

@router.get("/info")
def ai_info():

    return {
        "service": "AgriBridge AI",
        "provider": "Google Gemini",
        "status": "AI integration configured"
    }