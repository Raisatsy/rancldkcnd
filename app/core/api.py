from fastapi import APIRouter
from app.routers.client import router as client_router
from app.routers.operator import router as operator_router
from app.routers.ticket import router as ticket_router

api_router = APIRouter()

api_router.include_router(client_router, tags=["Client"])

api_router.include_router(operator_router, tags=["Operator"])

api_router.include_router(ticket_router, tags=["Ticket"])


