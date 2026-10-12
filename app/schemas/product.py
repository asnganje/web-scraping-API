from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name:str = Field(min_length=1, max_length=250)
    brand: str | None = Field(default=None, max_length=100)
    model_number:str | None= Field(default=None, max_length=100)
    category: str|None = Field(default=None, max_length=100)

class ProductResponse(BaseModel):
    id:int
    name:str
    brand:str|None
    model_number:str|None
    category:str|None
    is_active:bool

    model_config = {"from_attributes":True}

class ProductUpdate(BaseModel):
    name:str|None=Field(default=None, min_length=1, max_length=250)
    brand:str|None=Field(default=None, max_length=100)
    model_number:str|None=Field(default=None, max_length=100)
    category:str|None=Field(default=None, max_length=100)
    is_active:bool|None=None