from fastapi import APIRouter
from app.api.retailers import router as retailers_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(retailers_router)