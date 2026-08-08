from fastapi import FastAPI
from sqlalchemy import text

from backend.routers import farmers
from backend.routers import ai
from backend.core.database import engine

app = FastAPI(
    title="AgriBridge AI API",
    version="1.0.0"
)

# Existing farmer routes
app.include_router(farmers.router)

# AgriBridge AI routes
app.include_router(ai.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to AgriBridge AI API!"
    }


@app.get("/db-test")
def test_database():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_database();")
        )
        db_name = result.scalar()

    return {
        "status": "Database connected successfully!",
        "database": db_name
    }