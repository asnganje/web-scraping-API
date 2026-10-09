from fastapi import FastAPI, status

from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description="API for web scraping, data processing, and Google Sheets automation",
    version="1.0.0"
)

@app.get("/", status_code=status.HTTP_200_OK, tags=["Home"])
def root():
    return {
        "message":"Welcome to the Web Scraping Intelligence API"
    }

