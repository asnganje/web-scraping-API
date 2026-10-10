from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class Retailer(Base):
    __tablename__ = "retailers"
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name:Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    website_url:Mapped[str]= mapped_column(String(500), unique=True, nullable=False)
    is_active:Mapped[bool]=mapped_column(Boolean, default=True, nullable=False)
