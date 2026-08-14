from sqlalchemy.orm import Session

from backend.models.ai_conversation import AIConversation


# =========================================================
# GET CONVERSATION HISTORY
# =========================================================

def get_conversation_history(
    db: Session,
    farmer_name: str,
    limit: int = 10
):
    """
    Retrieve the most recent conversation messages
    belonging to a farmer.
    """

    messages = (
        db.query(AIConversation)
        .filter(
            AIConversation.farmer_name == farmer_name
        )
        .order_by(
            AIConversation.created_at.desc()
        )
        .limit(limit)
        .all()
    )

    # Reverse the results so that the oldest message
    # appears first and the newest message appears last.
    messages.reverse()

    return messages
