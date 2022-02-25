from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import sys
import os

# Include root dir
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.dependencies.db import get_db_session
from app.database.base import database_url, Base
from app.main import app_fastapi


# Set up DB
database_url += '_test'
db_engine_test = create_async_engine(database_url)
db_session_test = sessionmaker(
    bind=db_engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Session testing dependency
async def get_db_session_test():
    loc_db_session: AsyncSession = db_session_test()

    try:
        yield loc_db_session
    finally:
        await loc_db_session.commit()
        await loc_db_session.close()


# Test events
@app_fastapi.on_event('startup')
async def event_startup(db: AsyncSession = Depends(get_db_session_test)):
    await db.run_sync(Base.metadata.create_all)


# Test dependencies
app_fastapi.dependency_overrides[get_db_session] = get_db_session_test
base_url = 'http://127.0.0.1:8000/'
