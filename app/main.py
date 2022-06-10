import sentry_sdk
from fastapi import FastAPI
from routes.user import router_user
from routes.auth import router_auth
from routes.client import router_client
from dependencies.settings import get_settings, Settings, Environment


app_fastapi = FastAPI()
app_fastapi.include_router(router_user)
app_fastapi.include_router(router_auth)
app_fastapi.include_router(router_client)


@app_fastapi.on_event('startup')
def startup(settings: Settings = get_settings()):
    if settings.environment == Environment.prod:
        # TODO: Check performance without sentry
        sentry_sdk.init(
            settings.sentry.url,
            traces_sample_rate=settings.sentry.traces_sample_rate,
        )
