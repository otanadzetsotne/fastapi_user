from fastapi import FastAPI

from app.routes import user_router
from app.database.base import db


# await db.Base.metadata.create_all(bind=db.engine)


app = FastAPI()
app.include_router(user_router)


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
