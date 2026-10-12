from fastapi import APIRouter
from app.api.retailers import router as retailers_router
from app.api.products import router as products_router
from app.api.retailer_listings import router as retailer_listings_router
from app.api.price_history import router as price_history_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(retailers_router)
api_router.include_router(products_router)
api_router.include_router(retailer_listings_router )
api_router.include_router(price_history_router)