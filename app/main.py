import sentry_sdk
from fastapi import FastAPI
from routes.user import router_user
from routes.auth import router_auth
from routes.client import router_client
from dependencies.settings import get_settings, Settings, Environment
from database.base import db_engine, Base


app_fastapi = FastAPI()
app_fastapi.include_router(router_user)
app_fastapi.include_router(router_auth)
app_fastapi.include_router(router_client)


def run_sentry(settings):
    if settings.environment == Environment.prod:
        # TODO: Check performance without sentry
        sentry_sdk.init(
            settings.sentry.url,
            traces_sample_rate=settings.sentry.traces_sample_rate,
        )


async def create_tables():
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await db_engine.dispose()


@app_fastapi.on_event('startup')
async def startup(settings: Settings = get_settings()):
    run_sentry(settings)
    await create_tables()
