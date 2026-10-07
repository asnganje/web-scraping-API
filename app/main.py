from fastapi import FastAPI, status

app = FastAPI(
    title="Web Scraping Intelligence API",
    description="API for web scraping, data processing, and Google Sheets automation",
    version="1.0.0"
)

@app.get("/", status_code=status.HTTP_200_OK, tags=["Home"])
def root():
    return {
        "message":"Welcome to the Web Scraping Intelligence API"
    }

