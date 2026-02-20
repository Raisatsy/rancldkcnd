from dishka import Provider, provide, Scope

from app.core.config import Settings, settings


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return settings