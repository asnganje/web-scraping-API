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
    available_retailer_listings=[
        (listing, retailer)
        for listing, retailer in results
        if listing.is_available is True
        and listing.current_price is not None
        and listing.currency == "KES"
    ]

    available_prices=[
        listing.current_price
        for listing, retailer in available_retailer_listings
    ]

    if available_prices:
        average_price=sum(available_prices) / len(available_prices)
        lowest_price=min(available_prices)
        highest_price=max(available_prices)

        lowest_listing, lowest_retailer=min(
            available_retailer_listings,
            key=lambda item:item[0].current_price
        )

        lowest_price_retailer = {
            "retailer_name":lowest_retailer.name,
            "price":lowest_listing.current_price,
            "product_url":lowest_listing.product_url
        }

    else:
        average_price = None
        lowest_price = None
        highest_price = None
        lowest_price_retailer = None


    return {
        "product":{
            "id":product.id,
            "name":product.name,
            "brand":product.brand,
            "model_number":product.model_number,
            "category":product.category
        },
        "retailer_prices":retailer_prices,
        "price_statistics":{
            "currency":"KES",
            "average_price":average_price,
            "lowest_price":lowest_price,
            "highest_price":highest_price,
            "retailer_count":len(available_prices),
            "lowest_price_retailer":lowest_price_retailer
        }
    }






