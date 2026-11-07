from datetime import datetime

from sqlalchemy import Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class ScrapingJobResult(Base):
    __tablename__ = "scraping_job_results"
    id:Mapped[int]=mapped_column(Integer, primary_key=True)
    job_id:Mapped[int]=mapped_column(ForeignKey("scraping_jobs.id"), nullable=False)
    spider_name:Mapped[str]=mapped_column(String(100), nullable=False)
    status:Mapped[str]=mapped_column(String(20), default="pending", nullable=False)
    started_at:Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
