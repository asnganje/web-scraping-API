from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class ScrapingJob(Base):
    __tablename__ = "scraping_jobs"
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    status:Mapped[str]=mapped_column(String(20), default="pending", nullable=False)
    started_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
