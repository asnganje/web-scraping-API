from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Retailer
from app.schemas.retailer import RetailerResponse, RetailerCreate, RetailerUpdate

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

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[RetailerResponse])
def get_retailers(db:Session=Depends(get_db)):
    statement = select(Retailer)
    results = db.execute(statement)
    retailers_output=results.scalars().all()
    return retailers_output

@router.get("/{retailer_id}", status_code=status.HTTP_200_OK, response_model=RetailerResponse)
def get_retailer(retailer_id:int, db:Session=Depends(get_db)):
    retailer = db.get(Retailer, retailer_id)
    if retailer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Retailer not found"
        )
    return retailer

@router.patch("/{retailer_id}", status_code=status.HTTP_200_OK, response_model=RetailerResponse)
def update_retailer(retailer_id:int, payload:RetailerUpdate, db:Session=Depends(get_db)):
    retailer = db.get(Retailer, retailer_id)
    if retailer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Retailer not found"
        )
    if payload.name is not None:
        existing_retailer = db.query(Retailer).filter(Retailer.name == payload.name).first()
        if existing_retailer and existing_retailer.id != retailer.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Retailer name is already taken"
            )
    if payload.website_url is not None:
        existing_website_url = db.query(Retailer).filter(Retailer.website_url == str(payload.website_url)).first()
        if existing_website_url and existing_website_url.id != retailer.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Retailer website already exists"
            )

    retailer_values = payload.model_dump(exclude_unset=True)
    for field, value in retailer_values.items():
        if field == "website_url" and value is not None:
            value = str(value)
        setattr(retailer, field, value)
    db.commit()
    db.refresh(retailer)
    return retailer

@router.delete("/{retailer_id}", status_code=status.HTTP_200_OK)
def delete_retailer(retailer_id:int, db:Session=Depends(get_db)):
    retailer = db.get(Retailer, retailer_id)
    if retailer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Retailer not found"
        )
    db.delete(retailer)
    db.commit()
    return  {"msg":"Retailer deleted successfully!"}


