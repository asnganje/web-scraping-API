from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal

class PriceHistoryCreate(BaseModel):
    listing_id:int=Field(gt=0)
    price:Decimal=Field(ge=0, max_digits=12, decimal_places=2)
    currency:str=Field(default="USD", min_length=3, max_length=3)

class PriceHistoryResponse(BaseModel):
    id:int
    listing_id: int
    price: Decimal
    currency: str
    observed_at:datetime

    model_config = {"from_attributes":True}

class PriceHistoryUpdate(BaseModel):
    listing_id:int|None=Field(default=None, gt=0)
    price:Decimal|None=Field(default=None, ge=0, max_digits=12, decimal_places=2)
    currency:str|None=Field(default=None, min_length=3, max_length=3)
    observed_at:datetime|None=Field(default=None)


