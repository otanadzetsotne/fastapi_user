from functools import cache

from settings import Settings, Environment


@cache
def get_settings() -> Settings:
    settings = Settings()

    if settings.environment == Environment.test:
        settings.db.name = settings.db.name_testing

    return settings
