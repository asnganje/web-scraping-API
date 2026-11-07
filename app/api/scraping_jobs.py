from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import ScrapingJob, ScrapingJobResult

router = APIRouter(
    prefix=("/scraping-jobs"),
    tags=["Scraping Jobs"]
)

SPIDERS = [
    "lappyworld",
    "digitonia",
    "fahavi"
]

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_scraping_job(db:Session=Depends(get_db)):
    try:
        job = ScrapingJob()

        db.add(job)
        db.flush()
        for spider in SPIDERS:
            spider_result=ScrapingJobResult(
                job_id=job.id,
                spider_name=spider
            )
            db.add(spider_result)
        db.commit()
        db.refresh(job)
        return {
            "msg":"Scraping job created successfully",
            "jod_id":job.id,
            "status":job.status
        }
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create scraping job"
        )


