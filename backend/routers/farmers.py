from fastapi import APIRouter

router = APIRouter(
    prefix="/farmers",
    tags=["Farmers"]
)

@router.get("/")
def get_farmers():
    return {
        "message": "List of farmers will appear here."
    }

@router.post("/")
def create_farmer():
    return {
        "message": "Farmer created successfully."
    }