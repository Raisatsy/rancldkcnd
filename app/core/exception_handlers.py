from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.logger import logger
from app.exceptions.client import ClientNotFound
from app.exceptions.operator import OperatorNotFound
from app.exceptions.ticket import TicketNotFound, TicketInvalidStatusTransition


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(ClientNotFound)
    async def client_not_found_handler(request: Request, exc: ClientNotFound):
        logger.info(f"Client not found: {exc.id}")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"detail": f"Client {exc.id} not found."})

    @app.exception_handler(OperatorNotFound)
    async def operator_not_found_handler(request: Request, exc: OperatorNotFound):
        logger.info(f"Operator not found: {exc.id}")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": f"Operator {exc.id} not found."})

    @app.exception_handler(TicketNotFound)
    async def ticket_not_found_handler(request: Request, exc: TicketNotFound):
        logger.info(f"Ticket not found: {exc.id}")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": f"Ticket {exc.id} not found."})

    @app.exception_handler(TicketInvalidStatusTransition)
    async def ticket_invalid_status_transition_handler(request: Request, exc: TicketInvalidStatusTransition):
        logger.info(f"Change status swap from {exc.old_status} to {exc.new_status}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": f"Change status swap from {exc.old_status} to {exc.new_status}"})