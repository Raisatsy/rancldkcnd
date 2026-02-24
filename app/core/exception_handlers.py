from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.logger import logger
from app.exceptions.client import ClientNotFound
from app.exceptions.operator import OperatorNotFound


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