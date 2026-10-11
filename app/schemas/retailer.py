from pydantic import BaseModel, Field, HttpUrl

class RetailerCreate(BaseModel):
    name:str=Field(min_length=1, max_length=150)
    website_url:HttpUrl=Field(max_length=500)

class RetailerUpdate(BaseModel):
    name:str|None=Field(default=None, min_length=1, max_length=150)
    website_url:HttpUrl|None=Field(default=None, max_length=500)
    is_active:bool|None=Field(default=None)

class RetailerResponse(BaseModel):
    id:int
    name:str
    website_url:HttpUrl
    is_active:bool

    model_config = {"from_attributes": True}
