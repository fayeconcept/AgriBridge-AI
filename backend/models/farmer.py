from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from backend.core.database import Base


class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    state = Column(String, nullable=False)
    lga = Column(String, nullable=False)
    farm_size = Column(Float, nullable=False)
    crop_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)