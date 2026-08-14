from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# =========================================
# DATABASE CONNECTION
# =========================================

DATABASE_URL = "postgresql://postgres:%40queenJ04%25@localhost:5432/agribridge_ai"


engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


# =========================================
# IMPORT DATABASE MODELS
# =========================================

from backend.models.farmer import Farmer
from backend.models.ai_conversation import AIConversation


# =========================================
# CREATE DATABASE TABLES
# =========================================

Base.metadata.create_all(bind=engine)