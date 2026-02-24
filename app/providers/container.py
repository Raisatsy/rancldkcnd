from dishka import AsyncContainer, make_async_container

from app.providers.config import ConfigProvider
from app.providers.db import DbProvider
from app.providers.repo import RepoProvider
from app.providers.services import ServiceProvider


def get_container() -> AsyncContainer:
    providers = [
        ConfigProvider(),
        DbProvider(),
        ServiceProvider(),
        RepoProvider()
    ]
    return make_async_container(*providers)