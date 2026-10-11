from sqlalchemy import Integer, ForeignKey, Numeric, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base
from decimal import Decimal
from datetime import datetime


class PriceHistory(Base):
    __tablename__ = "price_history"
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    listing_id:Mapped[int]=mapped_column(ForeignKey("retailer_listings.id"), nullable=False, index=True)
    price:Mapped[Decimal]=mapped_column(Numeric(12,2), nullable=False)
    currency:Mapped[str]=mapped_column(String(3), default="USD", nullable=False)
    observed_at:Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)