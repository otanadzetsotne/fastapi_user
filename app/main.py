from fastapi import FastAPI
from .routes.auth import router_auth


app_fastapi = FastAPI()
app_fastapi.include_router(router_auth)
