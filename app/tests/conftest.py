from typing import Any
from typing import Generator

import databases
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine

import sys
import os

# Include root dir
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database.base import database_url, metadata
from app.main import app_fastapi


# Set up DB
database_url += '_test'
db_test = databases.Database(database_url)
engine = create_async_engine(database_url)


# Set up events for new Database
@app_fastapi.on_event('startup')
async def startup():
    await metadata.create_all(engine)
    await db_test.connect()


@app_fastapi.on_event('shutdown')
async def shutdown():
    await metadata.drop_all(engine)
    await db_test.disconnect()


client = TestClient(app_fastapi)
