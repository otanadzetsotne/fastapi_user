from functools import cache

from ..settings import Settings


@cache
def get_settings() -> Settings:
    return Settings()
