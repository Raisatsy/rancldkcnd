from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.core.api import api_router
from app.core.exception_handlers import register_exception_handlers
from app.providers.container import get_container


def create_app() -> FastAPI:
    app = FastAPI()

    container = get_container()
    setup_dishka(container, app)

    app.include_router(api_router)
    register_exception_handlers(app)
    return app