from sqlalchemy import Column, Integer, String, DateTime
from backend.core.database import Base


class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone = Column(String, unique=True)
    email = Column(String, unique=True)
    farm_name = Column(String)
    location = Column(String)
    state = Column(String, nullable=False)
    lga = Column(String)
    farm_size = Column(String)
    crop_type = Column(String)
    created_at = Column(DateTime)