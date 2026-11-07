from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Product, Retailer, RetailerListing

router = APIRouter(prefix="/products", tags=["Price Comparison"])

@router.get("/{product_id}/price_comparison", status_code=status.HTTP_200_OK, response_model=dict)
def get_price_comparison(
        product_id:int,
        db:Session=Depends(get_db)
    ):

    product = db.get(Product, product_id)

    if Product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    query_statement = (select(RetailerListing, Retailer).
                       join(Retailer, RetailerListing.retailer_id == Retailer.id).
                       where(
                            RetailerListing.product_id == product_id,
                            RetailerListing.is_active.is_(True),
                            Retailer.is_active.is_(True)
                        )
                    )

    results = db.execute(query_statement).all()
    retailer_prices=[]

    for listing, retailer in results:
        retailer_prices.append({
            "retailer_id": retailer.id,
            "retailer_name":retailer.name,
            "listing_id":listing.id,
            "product_url": listing.product_url,
            "current_price":listing.current_price,
            "currency":listing.currency,
            "is_available":listing.is_available
        })

    return {
        "product":{
            "id":product.id,
            "name":product.name,
            "brand":product.brand,
            "model_number":product.model_number,
            "category":product.category
        },
        "retailer_prices":retailer_prices
    }






