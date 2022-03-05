from fastapi import FastAPI
from .routes.auth import router_auth
from .routes.client import router_client


app_fastapi = FastAPI()
app_fastapi.include_router(router_auth)
app_fastapi.include_router(router_client)
