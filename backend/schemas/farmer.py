from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FarmerCreate(BaseModel):
    full_name: str
    phone: str
    email: str
    farm_name: str
    location: str
    state: str
    lga: str
    farm_size: float
    crop_type: str


class FarmerResponse(BaseModel):
    id: int
    full_name: str
    phone: str
    email: str
    farm_name: str
    location: str
    state: str
    lga: str
    farm_size: float
    crop_type: str
    created_at: Optional[datetime] = None