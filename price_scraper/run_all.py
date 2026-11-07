import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models import ScrapingJob, ScrapingJobResult

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
SCRAPY_PROJECT_DIR = Path(__file__).resolve().parent

def get_db_session():
    return SessionLocal()

def update_job_status(job_id, status):
    db = get_db_session()

    try:
        job = db.get(ScrapingJob, job_id)

        if not job:
            raise ValueError(
                f"Scraping job {job_id} not found"
            )
        job.status = status
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
def update_spider_status(job_id, spider_name, status):
    db=get_db_session()

    try:
        query_statement = (select(ScrapingJobResult).
                           where(ScrapingJobResult.job_id == job_id,
                                 ScrapingJobResult.spider_name==spider_name
                                 )
                           )
        spider_result = db.execute(query_statement).scalar_one_or_none()
        if not spider_result:
            raise ValueError(
                f"Result for spider {spider_name} "
                f"in job {job_id} not found!"
            )
        spider_result.status = status
        if status == "running":
            spider_result.started_at = datetime.now(timezone.utc)
        if status in ("success", "failed"):
            spider_result.completed_at=datetime.now(timezone.utc)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()





SPIDERS = [
    "lappyworld",
    "digitonia",
    "fahavi"
]

spider_results = []
for spider in SPIDERS:
    print(f"\nStarting spider: {spider}")
    result = subprocess.run([
        sys.executable,
        "-m",
        "scrapy",
        "crawl",
        spider
        ],
        cwd=SCRAPY_PROJECT_DIR
    )

    status = "Success" if result.returncode == 0 else "Failed"
    spider_results.append({
        "spider":spider,
        "status":status
    })

print("\n=================SPIDERS SUMMARY=============")
for result in spider_results:
    print(f"{result["spider"]}: {result["status"]}")
print("=================================================")
