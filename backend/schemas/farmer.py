from pydantic import BaseModel


class FarmerCreate(BaseModel):
    full_name: str
    phone: str
    email: str
    farm_name: str
    location: str
    state: str