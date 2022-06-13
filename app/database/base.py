from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from dependencies.settings import get_settings


settings = get_settings()
Base = declarative_base()
db_engine = create_async_engine(settings.db.url)
db_session = sessionmaker(
    bind=db_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
