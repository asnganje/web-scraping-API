from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import PriceHistory, RetailerListing
from app.schemas.price_history import PriceHistoryResponse, PriceHistoryCreate

router = APIRouter(
    prefix="/price-history",
    tags=["Price History"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PriceHistoryResponse)
def create_price_observation(payload:PriceHistoryCreate, db:Session=Depends(get_db)):
    listing = db.get(RetailerListing, payload.listing_id)

    if listing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Retailer listing not found"
        )

    price_observation = PriceHistory(
        listing_id=payload.listing_id,
        price=payload.price,
        currency=payload.currency
    )

    listing.current_price = payload.price
    listing.currency = payload.currency

    db.add(price_observation)
    try:
        db.commit()
        db.refresh(price_observation)
    except Exception:
        db.rollback()
        raise

    return price_observation

@router.get("/retailer_listings/{listing_id}", status_code=status.HTTP_200_OK, response_model=list[PriceHistoryResponse])
def get_listing_price_history(listing_id:int, db:Session=Depends(get_db)):
    listing = db.get(RetailerListing, listing_id)
    if listing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Retailer listing not found"
        )

    statement = (select(PriceHistory)
                 .where(PriceHistory.listing_id == listing_id)
                 .order_by(PriceHistory.observed_at.asc())
                 )

    results = db.execute(statement)
    observed_price_histories = results.scalars().all()
    return observed_price_histories

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[PriceHistoryResponse])
def get_all_observed_price_history(db:Session=Depends(get_db)):
    statement = select(PriceHistory).order_by(PriceHistory.observed_at.desc())
    results = db.execute(statement)
    all_price_histories=results.scalars().all()
    return all_price_histories