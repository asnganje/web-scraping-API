from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import RetailerListing, Retailer, Product
from app.schemas.retailer_listing import RetailerListingCreate, RetailerListingResponse, RetailerListingUpdate

router = APIRouter(
    prefix="/retailer_listings",
    tags=["Retailer Listings"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RetailerListingResponse)
def create_retailer_listing(payload:RetailerListingCreate, db:Session=Depends(get_db)):
    retailer = db.get(Retailer, payload.retailer_id)
    if retailer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Retailer not found"
        )

    product = db.get(Product, payload.product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    existing_retailer = db.query(RetailerListing).filter(
        RetailerListing.product_url == str(payload.product_url)
    ).first()

    if existing_retailer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product URL already exists"
        )

    new_retailer_listing = RetailerListing(
        retailer_id=payload.retailer_id,
        product_id=payload.product_id,
        product_url=str(payload.product_url),
        current_price=payload.current_price,
        currency=payload.currency,
        is_available=payload.is_available
    )

    db.add(new_retailer_listing)
    db.commit()
    db.refresh(new_retailer_listing)
    return new_retailer_listing

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[RetailerListingResponse])
def get_retailer_listings(db:Session=Depends(get_db)):
    statement = select(RetailerListing)
    results = db.execute(statement)
    retailer_listings = results.scalars().all()
    return  retailer_listings

@router.get("/{retailer_listing_id}", status_code=status.HTTP_200_OK, response_model=RetailerListingResponse)
def get_retailer_listing(retailer_listing_id:int, db:Session=Depends(get_db)):
    retailer_listing = db.get(RetailerListing, retailer_listing_id)
    if retailer_listing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Retailer listing not found"
        )
    return retailer_listing

@router.patch("/{retailer_listing_id}", status_code=status.HTTP_200_OK, response_model=RetailerListingResponse)
def update_retailer_listing(retailer_listing_id:int, payload: RetailerListingUpdate, db:Session=Depends(get_db)):
    retailer_listing = db.get(RetailerListing, retailer_listing_id)
    if retailer_listing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Retailer listing not found"
        )

    if payload.retailer_id is not None:
        retailer = db.get(Retailer, payload.retailer_id)
        if retailer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Retailer not found"
            )
    if payload.product_id is not None:
        product = db.get(Product, payload.product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
    if payload.product_url is not None:
        existing_retailer_listing = db.query(RetailerListing).filter(
            RetailerListing.product_url == str(payload.product_url)).first()

        if existing_retailer_listing and existing_retailer_listing.id != retailer_listing.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product URL already exists"
            )

    updated_values = payload.model_dump(exclude_unset=True)
    for field, value in updated_values.items():
        if field == "product_url" and value is not None:
            value = str(value)
        setattr(retailer_listing, field, value)
    db.commit()
    db.refresh(retailer_listing)
    return retailer_listing

@router.delete("/retailer_listing_id", status_code=status.HTTP_200_OK, response_model=dict)
def delete_retailer_listing(retailer_listing_id:int, db:Session=Depends(get_db)):
    retailer_listing = db.get(RetailerListing, retailer_listing_id)
    if retailer_listing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Retailer listing not found"
        )
    db.delete(retailer_listing)
    db.commit()
    return {"msg":"Retailer listing deleted successfully"}
