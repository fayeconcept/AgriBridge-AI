from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from backend.core.database import Base


class AIConversation(Base):
    __tablename__ = "ai_conversations"

    id = Column(Integer, primary_key=True, index=True)

    farmer_name = Column(String, nullable=False)

    role = Column(String, nullable=False)

    content = Column(Text, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )