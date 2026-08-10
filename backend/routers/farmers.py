from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.core.database import SessionLocal
from backend.models.farmer import Farmer
from backend.schemas.farmer import FarmerCreate


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix="/farmers",
    tags=["Farmers"]
)


@router.get("/")
def get_farmers(db: Session = Depends(get_db)):
    farmers = db.query(Farmer).all()

    return farmers


@router.post("/")
def create_farmer(
    farmer: FarmerCreate,
    db: Session = Depends(get_db)
):
    new_farmer = Farmer(
    full_name=farmer.full_name,
    phone=farmer.phone,
    email=farmer.email,
    farm_name=farmer.farm_name,
    location=farmer.location,
    state=farmer.state,
    lga=farmer.lga,
    farm_size=farmer.farm_size,
    crop_type=farmer.crop_type
)

    db.add(new_farmer)
    db.commit()
    db.refresh(new_farmer)

    return {
        "message": "Farmer created successfully.",
        "id": new_farmer.id
    }