from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class Product(Base):
    __tablename__ = "products"
    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    name:Mapped[str]=mapped_column(String(250), nullable=False, unique=True)
    brand:Mapped[str|None]=mapped_column(String(100), nullable=True)
    model_number:Mapped[str|None]=mapped_column(String(100), nullable=True)
    category:Mapped[str|None]=mapped_column(String(100), nullable=True)
    is_active:Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
