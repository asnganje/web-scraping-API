import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from sqlalchemy import select

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.database.session import SessionLocal
from app.models import ScrapingJob, ScrapingJobResult


SCRAPY_PROJECT_DIR = Path(__file__).resolve().parent

SPIDERS = [
    "lappyworld",
    "digitonia",
    "fahavi"
]

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

        if status == "running":
            job.started_at = datetime.now(timezone.utc)
        if status in ("completed", "failed"):
            job.completed_at = datetime.now(timezone.utc)
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

def run_spiders(job_id):
    failed_spiders=[]
    update_job_status(job_id, "running")

    for spider in SPIDERS:

        print(f"\nStarting spider: {spider}")
        update_spider_status(job_id, spider, "running")
        try:
            result = subprocess.run([
                sys.executable,
                "-m",
                "scrapy",
                "crawl",
                spider
                ],
                cwd=SCRAPY_PROJECT_DIR
            )

            if result.returncode == 0:
                status = "success"
                print(f"Spider {spider} completed successfully")
            else:
                status = "failed"
                failed_spiders.append(spider)
                print(f"Spider {spider} failed")
        except Exception as exc:
            status = "failed"
            failed_spiders.append(spider)
            print(f"Error running spider {spider}: {exc}")
        update_spider_status(job_id, spider, status)
    if failed_spiders:
        update_job_status(job_id, "failed")
    else:
        update_job_status(job_id, "completed")

    print("\n=================SCRAPING JOB SUMMARY=============")
    for spider_updated in SPIDERS:
        print(f"{spider_updated}:{'failed' if spider_updated in failed_spiders else 'completed'}")
    print("=================================================")
    if failed_spiders:
        print("Overall job status: FAILED")
    else:
        print("Overall job status: COMPLETED")
    print("=================================================")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: A scraping job id is required")
        sys.exit(1)
    job_id=int(sys.argv[1])
    run_spiders(job_id)


