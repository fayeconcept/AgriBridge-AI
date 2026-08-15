from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from pathlib import Path

from backend.routers import farmers
from backend.routers import ai
from backend.core.database import engine


app = FastAPI(
    title="AgriBridge AI API",
    version="1.0.0"
)


# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================
# API ROUTES
# =========================================

app.include_router(farmers.router)
app.include_router(ai.router)


# =========================================
# DATABASE TEST
# =========================================

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


# =========================================
# FRONTEND
# =========================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


# Serve the frontend after the API routes
app.mount(
    "/",
    StaticFiles(
        directory=FRONTEND_DIR,
        html=True
    ),
    name="frontend"
)