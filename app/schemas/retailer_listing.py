from pydantic import BaseModel, Field, HttpUrl
from decimal import Decimal


class RetailerListingCreate(BaseModel):
    retailer_id:int = Field(gt=0)
    product_id:int = Field(gt=0)
    product_url:HttpUrl
    current_price:Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    currency:str=Field(default="USD", min_length=3, max_length=3)
    is_available:bool | None = None

class RetailerListResponse(BaseModel):
    id:int
    retailer_id:int
    product_id:int
    product_url:HttpUrl
    current_price: Decimal | None
    currency:str
    is_available:bool | None
    is_active:bool

class RetailerListingUpdate(BaseModel):
    retailer_id:int|None = Field(default=None, gt=0)
    product_id:int|None = Field(default=None, gt=0)
    product_url:HttpUrl|None = None
    current_price:Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    currency:str|None=Field(default=None, min_length=3, max_length=3)
    is_available:bool | None = None
    is_active:bool|None = None
