from fastapi import FastAPI, status

from app.api.router import api_router
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.app_name,
    description="API for web scraping, data processing, and Google Sheets automation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://price-intelligence-scraper.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/", status_code=status.HTTP_200_OK, tags=["Home"])
def root():
    return {
        "message":"Welcome to the Web Scraping Intelligence API"
    }

