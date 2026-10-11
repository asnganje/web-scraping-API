from sqlalchemy import Integer, ForeignKey, String, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal

from app.database.session import Base

class RetailerListing(Base):
    __tablename__ = "retailer_listings"
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    retailer_id:Mapped[int]=mapped_column(Integer, ForeignKey("retailers.id"), nullable=False)
    product_id:Mapped[int]=mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    product_url:Mapped[str]=mapped_column(String(1000), unique=True, nullable=False)
    current_price:Mapped[Decimal|None]=mapped_column(Numeric(12,2), nullable=True)
    currency:Mapped[str]=mapped_column(String(3), nullable=False, default="USD")
    is_available:Mapped[bool|None]=mapped_column(Boolean, nullable=True)
    is_active:Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

