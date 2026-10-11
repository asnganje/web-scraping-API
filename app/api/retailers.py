from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Retailer
from app.schemas.retailer import RetailerResponse, RetailerCreate

router = APIRouter(
    prefix="/retailers",
    tags=["Retailers"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RetailerResponse)
def create_retailer(payload:RetailerCreate, db:Session=Depends(get_db)):
    existing_retailer = db.query(Retailer).filter(Retailer.name == payload.name).first()
    if existing_retailer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Retailer name already exists"
        )

    existing_website_url = db.query(Retailer).filter(Retailer.website_url == str(payload.website_url)).first()
    if existing_website_url:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Retailer website already exists"
        )

    new_retailer = Retailer(
        name=payload.name,
        website_url=str(payload.website_url)
    )
    db.add(new_retailer)
    db.commit()
    db.refresh(new_retailer)
    return new_retailer
