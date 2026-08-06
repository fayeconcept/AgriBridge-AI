from fastapi import FastAPI
from backend.routers import farmers

app = FastAPI(
    title="AgriBridge AI API",
    version="1.0.0"
)

app.include_router(farmers.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to AgriBridge AI API!"
    }