from fastapi import FastAPI

from .database.base import db
from .routes.auth import router_auth


app_fastapi = FastAPI()
app_fastapi.include_router(router_auth)


@app_fastapi.on_event('startup')
async def startup():
    await db.connect()


@app_fastapi.on_event('shutdown')
async def shutdown():
    await db.disconnect()
