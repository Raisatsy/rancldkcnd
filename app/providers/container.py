from dishka import AsyncContainer, make_async_container

from app.providers.config import ConfigProvider
from app.providers.db import DbProvider


def get_container() -> AsyncContainer:
    providers = [
        ConfigProvider(),
        DbProvider()
    ]
    return make_async_container(*providers)