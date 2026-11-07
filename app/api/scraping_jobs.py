from pathlib import Path
import subprocess
import sys
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import ScrapingJob, ScrapingJobResult, RetailerListing, Retailer, Product

SCRAPY_PROJECT_DIR = (
    Path(__file__).resolve().parents[2] / "price_scraper"
)

RUNNER_PATH=SCRAPY_PROJECT_DIR / "run_all.py"



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

        subprocess.Popen(
            [
                sys.executable,
                str(RUNNER_PATH),
                str(job.id)
            ],
            cwd=SCRAPY_PROJECT_DIR
        )

        return {
            "msg":"Scraping job created successfully",
            "jod_id":job.id,
            "status":job.status
        }
    except Exception as exc:
        db.rollback()
        print(f"Error: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create scraping job"
        )

@router.get("/", status_code=status.HTTP_200_OK)
def get_scraping_jobs(db: Session = Depends(get_db)):

    query_statement = (
        select(ScrapingJob)
        .order_by(ScrapingJob.created_at.desc())
    )

    jobs = db.execute(query_statement).scalars().all()

    return [
        {
            "id": job.id,
            "status": job.status,
            "created_at": job.created_at,
            "started_at": job.started_at,
            "completed_at": job.completed_at
        }
        for job in jobs
    ]

@router.get("/{job_id}", status_code=status.HTTP_200_OK)
def get_scraping_job(job_id:int, db:Session=Depends(get_db)):
    job = db.get(ScrapingJob, job_id)

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scraping job not found"
        )

    query_statement = (select(ScrapingJobResult).
                       where(ScrapingJobResult.job_id == job.id).
                       order_by(ScrapingJobResult.id)
                       )
    spider_results = db.execute(query_statement).scalars().all()

    spider_retailers = {
        "lappyworld": "Laptops World",
        "digitonia": "Digitonia Systems Ltd",
        "fahavi": "Fahavi Computers"
    }
    spiders = []

    for spider in spider_results:
        retailer_name=spider_retailers.get(spider.spider_name)
        retailer = None
        listings = []
        if retailer_name:
            retailer = (db.execute(select(Retailer).
                        where(Retailer.name == retailer_name)).
                        scalar_one_or_none())
            if retailer:
                listing_statement=(
                    select(RetailerListing, Product).
                    join(Product, RetailerListing.product_id == Product.id).
                    where(RetailerListing.retailer_id == retailer.id,
                          RetailerListing.is_active.is_(True)
                          )
                )

                listing_results = db.execute(listing_statement).all()
                for listing, product in listing_results:
                    listings.append({
                        "product_id": product.id,
                        "product_name": product.name,
                        "current_price": listing.current_price,
                        "currency": listing.currency,
                        "is_available": listing.is_available,
                        "product_url": listing.product_url
                    })
        spiders.append({
            "spider_name": spider.spider_name,
            "status": spider.status,
            "started_at": spider.started_at,
            "completed_at": spider.completed_at,
            "retailer": retailer.name if retailer else None,
            "listings": listings
        })

    return {
        "id": job.id,
        "status": job.status,
        "created_at": job.created_at,
        "started_at": job.started_at,
        "completed_at": job.completed_at,
        "spiders":spiders
    }

