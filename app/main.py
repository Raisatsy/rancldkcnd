from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.providers.container import get_container


def create_app() -> FastAPI:
    app = FastAPI()

    container = get_container()
    setup_dishka(container, app)
    return app