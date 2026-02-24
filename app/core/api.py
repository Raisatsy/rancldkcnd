from fastapi import APIRouter
from app.routers.client import router as client_router

api_router = APIRouter()

api_router.include_router(client_router, tags=["Client"])

