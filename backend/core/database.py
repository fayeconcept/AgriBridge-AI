import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# =========================================
# DATABASE CONNECTION
# =========================================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")


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